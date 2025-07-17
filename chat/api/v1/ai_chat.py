from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from deps.auth import get_current_user
from services.chat_service import chat_service
from utils.resp import resp_success

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str


@router.post("/")
def chat_api(data: ChatRequest, user=Depends(get_current_user)):
    # return {"msg": "pong"}
    return resp_success(data="dasds") 

    # reply = chat_service.chat(data.prompt)
    # return {"msg": "pong"}

    # return ChatResponse(response=reply) 