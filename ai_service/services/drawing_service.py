from datetime import datetime

from dashscope import ImageSynthesis
from http import HTTPStatus

from sqlalchemy import desc

from models.ai import Drawing
from sqlalchemy.orm import Session


def create_drawing_task(db: Session, user_id: int, platform: str, model: str, prompt: str, size: str, rsp,
                        options: str = None):
    # 写入数据库
    drawing = Drawing(
        user_id=user_id,
        platform=platform,
        model=model,
        prompt=prompt,
        width=int(size.split('x')[0]),
        height=int(size.split('x')[1]),
        create_time=datetime.now(),
        update_time=datetime.now(),
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
    status = ImageSynthesis.fetch(drawing.task_id)
    if status.status_code == HTTPStatus.OK:
        # 可根据 status.output.task_status 更新数据库
        drawing.status = status.output.task_status
        if hasattr(status.output, 'results') and status.output.results:
            drawing.pic_url = status.output.results[0].url
        db.commit()
        db.refresh(drawing)
        return drawing, None
    else:
        return None, status.message


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