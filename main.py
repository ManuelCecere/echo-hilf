import os
import config.config_file
import openai
from fastapi import FastAPI

# Set OpenAI key
openai.api_key = os.environ["OPENAI_KEY"]
os.environ["COHERE_API_KEY"] = "avvPTkbPSOEpMuEZ7iWEFAsW2yFCFZQuc8EG9kCl"

from src.api import chat_router
import uvicorn

app = FastAPI()

app.include_router(chat_router.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
