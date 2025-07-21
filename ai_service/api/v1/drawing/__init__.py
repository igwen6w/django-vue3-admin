import json
import os

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import get_db
from deps.auth import get_current_user
from llm.factory import get_adapter
from services.drawing_service import get_drawing_page, create_drawing_task, fetch_drawing_task_status

router = APIRouter(prefix="/drawing", tags=["drawing"])

@router.get("/")
def api_get_image_page(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = get_drawing_page(db, user_id=user["user_id"], page=page, page_size=page_size)
    # 序列化 items
    data["items"] = [
        {
            "id": img.id,
            "prompt": img.prompt,
            "pic_url": img.pic_url,
            "status": img.status,
            "error_message": img.error_message,
            "created_at": img.created_at if hasattr(img, 'created_at') else None
        }
        for img in data["items"]
    ]
    return data

class CreateDrawingTaskRequest(BaseModel):
    prompt: str
    style: str = 'auto'
    size: str = '1024x1024'
    model: str = 'wanx_v1'
    platform: str = 'tongyi'
    n: int = 1


@router.post("/")
def api_create_image_task(
    req: CreateDrawingTaskRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_id = user["user_id"]
    style = req.style
    size = req.size
    platform = req.platform
    n = req.n
    prompt = req.prompt
    model = req.model
    print(user_id, req.platform, req.size, req.model, req.prompt)
    api_key = os.getenv("DASHSCOPE_API_KEY")
    adapter = get_adapter('tongyi', api_key=api_key, model=model)
    try:
        # rsp = adapter.create_drawing_task(prompt=prompt, n=n, style=style, size=size)
        # print(rsp, 'rsp')
        res_json = {
            "status_code": 200,
            "request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
            "code": "",
            "message": "",
            "output": {
                "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
                "task_status": "PENDING",
                "results": []
            },
            "usage": None
        }
        rsp = res_json
        if rsp['status_code'] != 200:
            raise HTTPException(status_code=500, detail=rsp['message'])
        option = {
            'style': style
        }
        drawing = create_drawing_task(
            db=db,
            user_id=user["user_id"],
            platform=platform,
            model=model,
            rsp=rsp,
            prompt=prompt,
            size=size,
            options=json.dumps(option)
        )
        return {"id": drawing.id, "task_id": drawing.task_id, "status": drawing.status}
    except NotImplementedError:
        print("该服务商不支持图片生成")


@router.get("/{id}")
def api_fetch_image_task_status(
    id: int,
    db: Session = Depends(get_db)
):
    image, err = fetch_drawing_task_status(db, id)
    if not image:
        raise HTTPException(status_code=404, detail=err or "任务不存在")
    return {
        "id": image.id,
        "status": image.status,
        "pic_url": image.pic_url,
        "error_message": image.error_message
    }
