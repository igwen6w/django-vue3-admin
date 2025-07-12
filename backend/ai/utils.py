from ai.models import AIModel
from utils.models import CommonStatus
from asgiref.sync import sync_to_async

@sync_to_async
def get_first_available_ai_config():
    # 这里只取第一个可用的，可以根据实际业务加筛选条件
    ai = AIModel.objects.filter(status=CommonStatus.ENABLED).prefetch_related('key').first()
    if not ai:
        raise Exception('没有可用的AI配置')
    return ai.model, ai.key.api_key, ai.key.url