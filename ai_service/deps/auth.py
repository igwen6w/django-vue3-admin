from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from db.session import get_db
from models.user import AuthToken, DjangoUser


def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='未登录')

    token = auth.split(' ', 1)[1]
    token_obj = db.query(AuthToken).filter(AuthToken.key == token).first()
    if not token_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token无效或已过期')

    user = db.query(DjangoUser).filter(DjangoUser.id == token_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户不存在')
    return {"user_id": user.id, "username": user.username, "email": user.email}