from sentence_transformers import SentenceTransformer, util
from tavily import TavilyClient
import json
import os
from pathlib import Path
import weaviate
from dotenv import load_dotenv
import dspy

load_dotenv()


FAQ_COLLECTION_NAME = "getSolarFAQ"
weaviate_port = int(os.getenv("WEAVIATE_PORT"))
weaviate_host = os.getenv("WEAVIATE_HOST")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = weaviate.connect_to_local(
    host=weaviate_host,
    port=weaviate_port,
)

def faqRetrieval(user_query: str):

    """
    Retrieves the most relevant answer from an FAQ database based on the user's query.
    """

    with open(Path(__file__).parent / "faq.json", "r") as f:
        faq_db = json.load(f)

    faq_questions = list(faq_db.keys())
    model = SentenceTransformer('all-MiniLM-L6-v2')
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

    query_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, faq_embeddings)[0]

    best_idx = scores.argmax().item()

    if scores[best_idx] > 0.5:
        return faq_db[faq_questions[best_idx]]
    return ""

def vectorRetrieval(user_query: str, limit: int = 3):
    """
    Retrieves the most relevant answer from a vector database based on the user's query.
    """

    collection = client.collections.get(FAQ_COLLECTION_NAME)
    response = collection.query.hybrid(
        query = user_query,
        limit = limit
    )

    # 3) Pull out the “content” property
    chunks = []
    for obj in response.objects:
        # adjust this depending on your client:
        content = obj.properties.get("content")  
        if content:
            chunks.append(content)

    return "\n\n".join(chunks)


def webSearch(user_query: str, limit: int = 5):
    """
    Run a web search and return the content from the top 5 search results
    """
    search_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = search_client.search(user_query, max_results=5)

    return [r["content"] for r in response["results"]]








    


