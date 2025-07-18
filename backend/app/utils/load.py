import os
from pathlib import Path
import re
import math
from typing import List
import nltk
from dotenv import load_dotenv
from docx import Document  # type: ignore
from PyPDF2 import PdfReader  # type: ignore
import logging
import weaviate 
import weaviate.classes as wvc  # type: ignore
from weaviate.classes.config import Configure  # type: ignore



load_dotenv()
nltk.download("punkt")  # Download the Punkt tokenizer model for sentence tokenizatio
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "app" / "data"

OPENAPI_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT"))
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST")
headers = {"X-OpenAI-Api-Key": OPENAPI_KEY}

FAQ_FILENAME = "gtSolar_product_specs.txt"
CRITERIA_FILENAME = "getSolar_lead_evaluation_criteria.txt"

client = weaviate.connect_to_local(
    host=WEAVIATE_HOST, port=WEAVIATE_PORT, headers=headers
)

def chunk_text(
    text: str,
    max_chars: int = 100,
    overlap: int = 50
) -> List[str]:
    """
    Splits a long string into chunks of up to max_chars, 
    with optional overlap to preserve context.
    """
    # First, split on sentence boundaries to avoid chopping mid-sentence:
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) <= max_chars:
            current += ("" if current == "" else " ") + sent
        else:
            if current:
                chunks.append(current)
            # start new chunk, optionally carrying overlap
            overlap_text = current[-overlap:] if overlap and len(current) > overlap else ""
            current = overlap_text + sent
    if current:
        chunks.append(current)
    return chunks



def store_documents():
    """
    Loads data from /data/documents into the Weaviate vector store database.
    Stores all document chunks in one collection named 'faq_data'.
    """

    chunks_list = []
    faq_chunks = []
    criteria_chunks = []

    processed_files = 0
    skipped_files = 0
    failed_files = []

    logger.info("Chunking Data...")

    for file_path in DATA_DIR.iterdir():
        filename = file_path.name
        file_path = os.path.join(DATA_DIR, filename)
        text = ""  # Initialize text variable

        try:
            # Handle different file types
            if filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

            elif filename.endswith(".pdf"):
                with open(file_path, "rb") as file:
                    pdf_reader = PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text

            elif filename.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])

            else:
                logger.warning(f"Skipping unsupported file format: {filename}")
                skipped_files += 1
                continue

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):
                data_properties = {
                    "filename": filename,
                    "content": chunk,
                    "chunk_index": i,
                }
                obj = wvc.data.DataObject(properties=data_properties)
                if filename == FAQ_FILENAME:
                    faq_chunks.append(obj)
                else:
                    criteria_chunks.append(obj)

            processed_files += 1
        
        except Exception as e:
            logger.error(f"Failed to process file {filename}: {e}")
            failed_files.append({"filename": filename, "error": str(e)})

    faq_collection_name = "getSolarFAQ"
    criteria_collection_name = "getSolarLeadCriteria"


    if client.collections.exists(faq_collection_name):
        client.collections.delete(faq_collection_name)
    
    if client.collections.exists(criteria_collection_name):
        client.collections.delete(criteria_collection_name)
    
    logger.info("Creating Schema 'getSolar faq data'...")
    properties = [
        wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="filename", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),
    ]
    client.collections.create(
        name=faq_collection_name,
        properties=properties,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_openai(
                name="openai_text_vectoriser",
                source_properties=[prop.name for prop in properties],
                model="text-embedding-3-large",
                type_="text",
                dimensions=1024,
            )
        ],
)
    
    if faq_chunks:
        logger.info(
            f"Inserting {len(faq_chunks)} chunks into the 'getSolar' collection..."
        )
        client.collections.get(faq_collection_name).data.insert_many(faq_chunks)
        logger.info(
            f"Successfully added {len(faq_chunks)} objects to the 'faq getSolar' collection."
        )
    
    
    logger.info("Creating Schema 'lead_evaluation_criteria'...")
    properties = [
        wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="filename", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),
    ]
    client.collections.create(
        name=criteria_collection_name,
        properties=properties,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_openai(
                name="openai_text_vectoriser",
                source_properties=[prop.name for prop in properties],
                model="text-embedding-3-large",
                type_="text",
                dimensions=1024,
            )
        ],
)
    
    if criteria_chunks:
        logger.info(
            f"Inserting {len(criteria_chunks)} chunks into the 'lead_evaluation_criteria' collection..."
        )
        client.collections.get(criteria_collection_name).data.insert_many(criteria_chunks)
        logger.info(
            f"Successfully added {len(criteria_chunks)} objects to the 'lead_evaluation_criteria' collection."
        )



    return {
        "processed_files": processed_files,
        "skipped_files": skipped_files,
        "failed_files": failed_files,
        "inserted_faq_chunks": len(faq_chunks),
        "inserted_criteria_chunks": len(criteria_chunks),
    }

if __name__ == "__main__":
    try:
        store_documents()
    finally:
        logger.info("Weaviate client connection closed.")
        client.close()



