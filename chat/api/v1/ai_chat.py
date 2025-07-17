import os
import asyncio

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from pydantic import BaseModel
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI

from deps.auth import get_current_user
from services.chat_service import ChatDBService
from db.session import get_db
from models.ai import ChatConversation, ChatMessage

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
async def chat_stream(request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
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

@router.get('/conversations')
def get_conversations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """获取当前用户的聊天对话列表"""
    user_id = user["user_id"]
    conversations = db.query(ChatConversation).filter(ChatConversation.user_id == user_id).order_by(ChatConversation.update_time.desc()).all()
    return [
        {
            'id': c.id,
            'title': c.title,
            'update_time': c.update_time,
            'last_message': c.messages[-1].content if c.messages else '',
        }
        for c in conversations
    ]

@router.get('/messages')
def get_messages(
    conversation_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """获取指定会话的消息列表（当前用户）"""
    user_id = user["user_id"]
    query = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id, ChatMessage.user_id == user_id)
    messages = query.order_by(ChatMessage.id).all()
    return [
        {
            'id': m.id,
            'role': m.role_id,
            'content': m.content,
            'user_id': m.user_id,
            'conversation_id': m.conversation_id,
            'create_time': m.create_time,
        }
        for m in messages
    ]