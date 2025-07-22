from pydantic import BaseModel


class CreateDrawingTaskRequest(BaseModel):
    prompt: str
    style: str = 'auto'
    size: str = '1024*1024'
    model: str = 'wanx_v1'
    platform: str = 'tongyi'
    n: int = 1
