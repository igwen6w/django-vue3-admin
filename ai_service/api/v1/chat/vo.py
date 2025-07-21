from pydantic import BaseModel
from datetime import datetime

class MessageVO(BaseModel):
    id: int
    content: str
    conversation_id: int
    type: str

    class Config:
        from_attributes = True  # 启用ORM模式支持

class ConversationsVO(BaseModel):
    id: int
    title: str
    update_time: datetime
    last_message: str | None = None
    
    class Config:
        from_attributes = True