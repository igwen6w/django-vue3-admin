from datetime import datetime

from db.session import Base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
)

# 基础模型类
class CoreModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    remark = Column(String(256), nullable=True, comment="备注")
    creator = Column(String(64), nullable=True, comment="创建人")
    modifier = Column(String(64), nullable=True, comment="修改人")

    # 创建时间 - 使用函数默认值，在插入时自动生成
    create_time = Column(DateTime, default=datetime.now(), comment="创建时间")

    # 修改时间 - 使用SQL函数，在更新时自动触发
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment="修改时间")

    is_deleted = Column(Boolean, default=False, comment="是否软删除")

    # 软删除方法
    # def soft_delete(self, session):
    #     self.is_deleted = True
    #     self.modifier = get_current_user()  # 需要实现这个函数获取当前用户
    #     self.update_time = datetime.utcnow()
    #     session.commit()

    # 查询时自动过滤已删除记录
    @classmethod
    def get_active(cls, session):
        return session.query(cls).filter(cls.is_deleted == False)