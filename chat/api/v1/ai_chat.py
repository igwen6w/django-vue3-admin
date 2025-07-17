import os
import asyncio

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from deps.auth import get_current_user
from services.chat_service import chat_service
from utils.resp import resp_success

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str


def get_deepseek_llm(api_key: str, model: str, openai_api_base: str):
    # deepseek 兼容 OpenAI API，需指定 base_url
    return ChatOpenAI(
        openai_api_key=api_key,
        model_name=model,
        streaming=True,
        openai_api_base=openai_api_base,   # deepseek的API地址
    )

@router.post('/stream')
async def chat_stream(request: Request):
    body = await request.json()
    content = body.get('content')
    print(content, 'content')
    model = 'deepseek-chat'
    api_key = os.getenv("DEEPSEEK_API_KEY")
    openai_api_base="https://api.deepseek.com/v1"
    llm = get_deepseek_llm(api_key, model, openai_api_base)

    if not content or not isinstance(content, str):
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "content不能为空"}, status_code=400)

    async def event_generator():
        async for chunk in llm.astream(content):
            # 只返回 chunk.content 内容
            if hasattr(chunk, 'content'):
                yield f"data: {chunk.content}\n\n"
            else:
                yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type='text/event-stream')