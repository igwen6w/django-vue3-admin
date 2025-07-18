from pydantic import BaseModel

class ChatCreate(BaseModel):
    pass

class Chat(ChatCreate):
    id: int

    class Config:
        orm_mode = True