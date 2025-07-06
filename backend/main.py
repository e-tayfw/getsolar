import os
import logging
import time
from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from app.routers.fastapi import rag_router

import mlflow
import mlflow.dspy



app = FastAPI(title="GetSolar AI API")

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set


if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def read_root():
    return "Welcome to the FastAPI application!"

app.include_router(
    rag_router, prefix="/solar", tags=["solar"]
)

if __name__ == "__main__":
    tracking_uri = "http://mlflow:5000"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("DSPy Get Solar AI Support")
    mlflow.dspy.autolog()
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True, reload_dirs=["app"])

