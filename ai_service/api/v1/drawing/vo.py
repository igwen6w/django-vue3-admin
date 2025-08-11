from pydantic import BaseModel
from llm.enums import LLMProvider


class CreateDrawingTaskRequest(BaseModel):
    prompt: str
    style: str = 'auto'
    size: str = '1024*1024'
    model: str = 'wanx_v1'
    platform: str = LLMProvider.TONGYI
    n: int = 1
