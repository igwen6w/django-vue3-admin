import os
from datetime import datetime

from dashscope import ImageSynthesis
from http import HTTPStatus

from sqlalchemy import desc

from llm.factory import get_adapter
from llm.enums import LLMProvider
from models.ai import Drawing
from sqlalchemy.orm import Session


def create_drawing_task(db: Session, user, platform: str, model: str, prompt: str, size: str, rsp,
                        options: str = None):
    # 写入数据库

    drawing = Drawing(
        user_id=user['user_id'],
        creator=user['username'],
        modifier=user['username'],
        platform=platform,
        model=model,
        prompt=prompt,
        width=int(size.split('*')[0]),
        height=int(size.split('*')[1]),
        options=options,
        status=rsp['output']['task_status'],
        task_id=rsp['output']['task_id'],
        error_message=rsp['message']
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)
    return drawing

def fetch_drawing_task_status(db: Session, drawing_id: int):
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing or not drawing.task_id:
        return None, "任务不存在"
    if drawing.status in ("PENDING", 'RUNNING'):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        adapter = get_adapter(LLMProvider.TONGYI, api_key=api_key, model='')
        rsp = adapter.fetch_drawing_task_status(drawing.task_id)
        if rsp['status_code'] == HTTPStatus.OK:
            # 可根据 status.output.task_status 更新数据库
            if rsp['output']['task_status'] == 'SUCCEEDED':
                drawing.update_time = datetime.now()
                drawing.status = rsp['output']['task_status']
                drawing.pic_url = rsp['output']['results'][0]['url']
                db.commit()
                db.refresh(drawing)
            elif rsp['output']['task_status'] == 'FAILED':
                drawing.update_time = datetime.now()
                drawing.status = rsp['output']['task_status']
                drawing.error_message = rsp['output']['message']
                db.commit()
                db.refresh(drawing)
            elif rsp['output']['task_status'] == 'RUNNING':
                drawing.update_time = datetime.now()
                drawing.status = rsp['output']['task_status']
                db.commit()
                db.refresh(drawing)
        return drawing, None
    else:
        return drawing, None


def get_drawing_page(db: Session, user_id: int = None, page: int = 1, page_size: int = 12):
    query = db.query(Drawing)
    if user_id:
        query = query.filter(Drawing.user_id == user_id)
    total = query.count()
    items = query.order_by(desc(Drawing.id)).offset((page - 1) * page_size).limit(page_size).all()
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'items': items
    } 