from asyncio.log import logger
import io
import os
import shutil
from app.utils.load import store_documents
from app.utils.models import QueryRequest
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi import UploadFile
from app.utils.functions import chat

rag_router = APIRouter()

@rag_router.get("/health")
async def health_check():
    try:
        return {"status": "ok"}
    except Exception as e:
        print(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed.")

@rag_router.post("/uploadfile")
async def upload_file(file: UploadFile):
    # Define allowed extensions
    allowed_extensions = {".txt", ".pdf", ".docx", ".xlsx"}

    # Check if file extension is allowed
    file_extension = file.filename.split(".")[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type is not allowed. Please upload a .txt, .pdf, .docx, or .xlsx file.")
    
    folder = "sources"
    try:
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.filename)
        file_content = await file.read()
        with open(file_path, "wb+") as file_object:
            file_like_object = io.BytesIO(file_content)
            shutil.copyfileobj(file_like_object, file_object)

        return {"filename": file.filename, "message": "File uploaded successfully."}

    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while uploading the file.")
    
@rag_router.post("/store-documents")
async def store_documents_endpoint():
    return store_documents()

@rag_router.post("/chat")
async def chat_endpoint(request: QueryRequest):
    return await chat(request)




    
