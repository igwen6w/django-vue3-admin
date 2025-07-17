from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.ai import AIApiKey  # SQLAlchemy模型
from schemas.ai_api_key import AIApiKeyCreate, AIApiKeyUpdate

# 继承通用CRUD基类，指定模型和Pydantic类型
class CRUDApiKey(CRUDBase[AIApiKey, AIApiKeyCreate, AIApiKeyUpdate]):
    # 如有特殊逻辑，可重写父类方法（如创建时验证平台唯一性）
    def create(self, db: Session, *, obj_in: AIApiKeyCreate):
        # 示例：验证平台+名称唯一
        if self.get_by(db, platform=obj_in.platform, name=obj_in.name):
            raise HTTPException(status_code=400, detail="该平台下名称已存在")
        return super().create(db, obj_in=obj_in)

# 创建CRUD实例
ai_api_key_crud = CRUDApiKey(AIApiKey)