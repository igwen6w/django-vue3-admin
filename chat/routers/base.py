from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, List

from db.session import get_db
from schemas.base import ReadSchemaType  # 通用的响应模型基类
from crud.base import CRUDBase

# 泛型变量（对应：CRUD类、创建模型、更新模型、响应模型）
CRUDType = TypeVar("CRUDType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ReadSchemaType = TypeVar("ReadSchemaType")


class GenericRouter(
    APIRouter,
    Generic[CRUDType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]
):
    def __init__(
        self,
        crud: CRUDType,
        create_schema: CreateSchemaType,
        update_schema: UpdateSchemaType,
        read_schema: ReadSchemaType,
        prefix: str,
        tags: List[str],
        **kwargs
    ):
        """
        初始化通用路由
        :param crud: CRUD实例（如CRUDApiKey）
        :param create_schema: 创建Pydantic模型
        :param update_schema: 更新Pydantic模型
        :param read_schema: 响应Pydantic模型
        :param prefix: 路由前缀（如"/api/ai-api-keys"）
        :param tags: 文档标签
        """
        super().__init__(prefix=prefix, tags=tags,** kwargs)
        self.crud = crud
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.read_schema = read_schema

        # 注册通用路由
        self.add_api_route(
            "/",
            self.create,
            methods=["POST"],
            response_model=read_schema,
            status_code=201
        )
        self.add_api_route(
            "/",
            self.get_multi,
            methods=["GET"],
            response_model=List[read_schema]
        )
        self.add_api_route(
            "/{id}/",
            self.get,
            methods=["GET"],
            response_model=read_schema
        )
        self.add_api_route(
            "/{id}/",
            self.update,
            methods=["PUT"],
            response_model=read_schema
        )
        self.add_api_route(
            "/{id}/",
            self.remove,
            methods=["DELETE"]
        )

    # 创建
    def create(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
        return self.crud.create(db=db, obj_in=obj_in)

    # 按ID查询
    def get(self, id: int, db: Session = Depends(get_db)):
        obj = self.crud.get(db=db, id=id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"记录不存在")
        return obj

    # 分页查询
    def get_multi(self, page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        return self.crud.get_multi(db=db, page=page, limit=limit)

    # 更新
    def update(self, id: int, obj_in: UpdateSchemaType, db: Session = Depends(get_db)):
        obj = self.crud.get(db=db, id=id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"记录不存在")
        return self.crud.update(db=db, db_obj=obj, obj_in=obj_in)

    # 删除
    def remove(self, id: int, db: Session = Depends(get_db)):
        return self.crud.remove(db=db, id=id)