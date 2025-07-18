from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 基础模型（共享字段）
class AIApiKeyBase(BaseModel):
    name: str = Field(..., max_length=255, description="密钥名称")
    platform: str = Field(..., max_length=100, description="平台（如openai）")
    api_key: str = Field(..., max_length=255, description="API密钥")
    url: Optional[str] = Field(None, max_length=255, description="自定义API地址")
    status: int = Field(0, description="状态（0=禁用，1=启用）")

# 创建请求模型（无需ID和时间字段）
class AIApiKeyCreate(AIApiKeyBase):
    pass

# 更新请求模型（所有字段可选）
class AIApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    platform: Optional[str] = Field(None, max_length=100)
    api_key: Optional[str] = Field(None, max_length=255)
    url: Optional[str] = Field(None, max_length=255)
    status: Optional[int] = None

# 响应模型（包含数据库自动生成的字段）
class AIApiKeyRead(AIApiKeyBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # 支持ORM模型直接转换为响应
    class Config:
        from_attributes = True  # Pydantic v2用from_attributes，v1用orm_mode