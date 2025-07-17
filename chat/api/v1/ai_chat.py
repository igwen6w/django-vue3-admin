import os
import asyncio

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from pydantic import BaseModel
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI

from deps.auth import get_current_user
from services.chat_service import ChatDBService
from db.session import get_db

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
async def chat_stream(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    body = await request.json()
    content = body.get('content')
    conversation_id = body.get('conversation_id')
    model = 'deepseek-chat'
    api_key = os.getenv("DEEPSEEK_API_KEY")
    openai_api_base = "https://api.deepseek.com/v1"
    llm = get_deepseek_llm(api_key, model, openai_api_base)

    if not content or not isinstance(content, str):
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "content不能为空"}, status_code=400)

    user_id = user["user_id"]

    # 1. 获取或新建对话
    try:
        conversation = ChatDBService.get_or_create_conversation(db, conversation_id, user_id, model)
    except ValueError as e:
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": str(e)}, status_code=400)
    # 2. 插入当前消息
    ChatDBService.add_message(db, conversation, user_id, content)

    # 3. 查询历史消息，组装上下文
    history = ChatDBService.get_history(db, conversation.id)
    history_contents = [msg.content for msg in history]
    context = '\n'.join(history_contents)

    async def event_generator():
        async for chunk in llm.astream(context):
            # 只返回 chunk.content 内容
            if hasattr(chunk, 'content'):
                yield f"data: {chunk.content}\n\n"
            else:
                yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type='text/event-stream')