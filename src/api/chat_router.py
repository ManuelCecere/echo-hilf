import requests
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
import openai
from src.pydantic_models.chat_models import ChatRequest
from src.rag.inference.query_engine import ask_question, ask_question_stream
from config.config_file import config_obj


router = APIRouter()

asyncio.get_event_loop().set_debug(True)

# client = openai.Client(
#     base_url="http://sglang_service:30000/v1", api_key="EMPTY")


@router.post("/generate")
async def generate(request: ChatRequest):
    try:
        response = ask_question(request)
        return response
    except Exception as e:
        print(e)


@router.post("/generate_stream")
async def generate_stream(request: ChatRequest):
    try:
        response = ask_question_stream(request)
        return response
    except Exception as e:
        print(e)
