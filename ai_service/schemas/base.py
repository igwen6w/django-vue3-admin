from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReadSchemaType(BaseModel):
    """
    所有响应模型的基类，包含公共字段和ORM转换配置
    """
    id: int
    created_at: Optional[datetime] = None  # 数据创建时间（可选，部分模型可能没有）
    updated_at: Optional[datetime] = None  # 数据更新时间（可选）

    class Config:
        """
        配置Pydantic模型如何处理ORM对象：
        - from_attributes=True：支持直接从SQLAlchemy ORM模型转换（Pydantic v2）
        - 若使用Pydantic v1，需替换为 orm_mode=True
        """
        from_attributes = True