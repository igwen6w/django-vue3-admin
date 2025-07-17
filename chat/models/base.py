from db.session import Base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
)

# 基础模型类
class CoreModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
