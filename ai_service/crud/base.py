from typing import Generic, TypeVar, List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

# 定义泛型变量（分别对应：SQLAlchemy模型、创建Pydantic模型、更新Pydantic模型）
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        """
        初始化CRUD类，需要传入SQLAlchemy模型
        :param model: SQLAlchemy模型类（如AIApiKey、AIModel等）
        """
        self.model = model

    # 创建
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """创建一条记录"""
        obj_in_data = obj_in.model_dump()  # 解构Pydantic模型为字典

        # 自动填充时间字段（如果模型有created_at/updated_at）
        if hasattr(self.model, "created_at"):
            obj_in_data["created_at"] = datetime.now()
        if hasattr(self.model, "updated_at"):
            obj_in_data["updated_at"] = datetime.now()

        db_obj = self.model(**obj_in_data)  # 实例化模型
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 按ID查询
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """按ID查询单条记录"""
        return db.query(self.model).filter(self.model.id == id).first()

    # 按条件查询单条记录
    def get_by(self, db: Session, **kwargs) -> Optional[ModelType]:
        """按条件查询单条记录（如get_by(name="test")）"""
        return db.query(self.model).filter_by(**kwargs).first()

    # 分页查询所有
    def get_multi(
            self, db: Session, *, page: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """分页查询多条记录"""
        return db.query(self.model).offset(page).limit(limit).all()

    # 更新
    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """更新记录（支持Pydantic模型或字典）"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)  # 只更新提供的字段

        # 遍历更新字段
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        # 自动更新updated_at（如果模型有该字段）
        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.now()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 删除
    def remove(self, db: Session, *, id: int) -> ModelType:
        """删除记录"""
        obj = db.query(self.model).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__}不存在")
        db.delete(obj)
        db.commit()
        return obj