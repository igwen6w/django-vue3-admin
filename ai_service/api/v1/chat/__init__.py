import os
import asyncio
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from pydantic import BaseModel, SecretStr
from langchain.chains import ConversationChain

from api.v1.chat.vo import MessageVO
from deps.auth import get_current_user
from llm.factory import get_adapter
from llm.enums import LLMProvider
from services.chat_service import ChatDBService
from db.session import get_db
from models.ai import ChatConversation, ChatMessage
from utils.resp import resp_success, Response
from langchain_deepseek import ChatDeepSeek

router = APIRouter(prefix="/chat", tags=["chat"])

def get_deepseek_llm(api_key: SecretStr, model: str):
    # deepseek 兼容 OpenAI API，需指定 base_url
    return ChatDeepSeek(
        api_key=api_key,
        model=model,
        streaming=True,
    )

@router.post('/stream')
async def chat_stream(request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    body = await request.json()
    content = body.get('content')
    conversation_id = body.get('conversation_id')
    platform = body.get('platform')
    # 未来改从配置文件中获取
    if platform == 'tongyi':
        model = 'qwen-plus'
        api_key = os.getenv("DASHSCOPE_API_KEY")
        provider = LLMProvider.TONGYI
    else:
        # 默认使用 DeepSeek
        model = 'deepseek-chat'
        api_key = os.getenv("DEEPSEEK_API_KEY")
        provider = LLMProvider.DEEPSEEK
    llm = get_adapter(provider, api_key=api_key, model=model)

    if not content or not isinstance(content, str):
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "content不能为空"}, status_code=400)

    user_id = user["user_id"]
    # 1. 获取对话
    try:
        conversation = ChatDBService.get_conversation(db, conversation_id)
        conversation = db.merge(conversation)  # ✅ 防止 DetachedInstanceError
    except ValueError as e:
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": str(e)}, status_code=400)
    # 2. 插入当前消息
    ChatDBService.add_message(db, conversation, user_id, content)
    context = [
        ("system", "You are a helpful assistant")
    ]
    # 3. 查询历史消息，组装上下文
    history = ChatDBService.get_history(db, conversation.id)
    # === 新增：如果只有一条消息，更新 title ===
    if len(history) == 1:
        ChatDBService.update_conversation_title(db, conversation.id, content[:255])

    for msg in history:
        # 假设 msg.type 存储的是 'user' 或 'assistant'
        # role = msg.type if msg.type in ("user", "assistant") else "user"
        context.append((msg.type, msg.content))

    ai_reply = ""
    async def event_generator():
        nonlocal ai_reply
        async for chunk in llm.stream_chat(context):
            if hasattr(chunk, 'content'):
                ai_reply += chunk.content
                yield f"data: {chunk.content}\n\n"
            else:
                ai_reply += chunk
                yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)
        # 只保留最新AI回复
        if ai_reply:
            ChatDBService.insert_ai_message(db, conversation, user_id, ai_reply, model)

    return StreamingResponse(event_generator(), media_type='text/event-stream')

@router.post("/conversations")
async def create_conversation(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user),):
    body = await request.json()
    platform = body.get('platform')
    if platform == 'tongyi':
        model = 'qwen-plus'
        # provider = LLMProvider.TONGYI
    else:
        # 默认使用 DeepSeek
        model = 'deepseek-chat'
        # provider = LLMProvider.DEEPSEEK
    user_id = user["user_id"]
    conversation = ChatDBService.get_or_create_conversation(db, None, user_id, model, '新对话')
    return resp_success(data=conversation.id)
    
@router.get('/conversations')
async def get_conversations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """获取当前用户的聊天对话列表，last_message为字符串"""
    user_id = user["user_id"]
    conversations = db.query(ChatConversation).filter(ChatConversation.user_id == user_id).order_by(ChatConversation.update_time.desc()).all()
    return resp_success(data=[
        {
            'id': c.id,
            'title': c.title,
            'update_time': c.update_time,
            'last_message': c.messages[-1].content if c.messages else None,
        }
        for c in conversations
    ])


@router.get('/messages', response_model=Response[List[MessageVO]])
def get_messages(
    conversation_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """获取指定会话的消息列表（当前用户）"""
    user_id = user["user_id"]
    query = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id,
                                         ChatMessage.user_id == user_id).order_by(ChatMessage.id).all()
    return resp_success(data=query)

