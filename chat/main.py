from fastapi import FastAPI
from api.v1 import ai_chat
from fastapi.middleware.cors import CORSMiddleware
from routers.ai_api_key import router as ai_api_key_router

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
app.include_router(ai_chat.router, prefix="/chat/api/v1", tags=["chat"])
app.include_router(ai_api_key_router, tags=["chat"])

# 健康检查
@app.get("/ping")
def ping():
    return {"msg": "pong"}
