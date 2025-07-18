from sqlalchemy import Column, Integer, String, DateTime, Boolean

from db.session import Base


class AuthToken(Base):
    __tablename__ = 'authtoken_token'
    key = Column(String(40), primary_key=True)
    user_id = Column(Integer, nullable=False)
    created = Column(DateTime)


class DjangoUser(Base):
    __tablename__ = 'system_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    email = Column(String(254))
    password = Column(String(128))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
    date_joined = Column(DateTime)