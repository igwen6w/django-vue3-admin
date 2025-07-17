from schemas.ai_api_key import AIApiKeyCreate, AIApiKeyUpdate, AIApiKeyRead
from crud.ai_api_key import ai_api_key_crud
from routers.base import GenericRouter

# 继承通用路由基类，传入参数即可生成所有CRUD接口
router = GenericRouter(
    crud=ai_api_key_crud,
    create_schema=AIApiKeyCreate,
    update_schema=AIApiKeyUpdate,
    read_schema=AIApiKeyRead,
    prefix="/chat/api/ai-api-keys",
    tags=["AI API密钥"]
)