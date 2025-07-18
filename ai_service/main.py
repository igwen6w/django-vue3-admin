import os
from fastapi import FastAPI
from dotenv import load_dotenv
from api.v1 import ai_chat
from fastapi.middleware.cors import CORSMiddleware

# 加载.env环境变量，优先项目根目录
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8010",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(ai_chat.router, prefix="/api/ai/v1", tags=["chat"])

# 健康检查
@app.get("/ping")
def ping():
    return {"msg": "pong"}
