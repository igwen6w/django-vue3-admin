from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: str = None

    class Config:
        orm_mode = True 