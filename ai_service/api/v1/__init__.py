from fastapi import APIRouter
from .chat import router as chat_router
from .drawing import router as drawing_router
# from .video import router as video_router
# from .audio import router as audio_router
# from .multimodal import router as multimodal_router
# from .model_manage import router as model_manage_router
# from .knowledge import router as knowledge_router
# from .system import router as system_router
# from .user import router as user_router

api_v1_router = APIRouter(prefix="/api/ai/v1")

api_v1_router.include_router(chat_router)
api_v1_router.include_router(drawing_router)
# api_v1_router.include_router(video_router)
# api_v1_router.include_router(audio_router)
# api_v1_router.include_router(multimodal_router)
# api_v1_router.include_router(model_manage_router)
# api_v1_router.include_router(knowledge_router)
# api_v1_router.include_router(system_router)
# api_v1_router.include_router(user_router)