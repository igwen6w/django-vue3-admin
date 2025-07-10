from django.db import models


class PlatformChoices(models.TextChoices):
    AZURE_OPENAI = 'AzureOpenAI', 'OpenAI 微软'
    OPENAI = 'OpenAI', 'OpenAI'
    OLLAMA = 'Ollama', 'Ollama'
    YIYAN = 'YiYan', '文心一言'
    XINGHUO = 'XingHuo', '讯飞星火'
    TONGYI = 'TongYi', '通义千问'
    STABLE_DIFFUSION = 'StableDiffusion', 'StableDiffusion'
    MIDJOURNEY = 'Midjourney', 'Midjourney'
    SUNO = 'Suno', 'Suno'
    DEEPSEEK = 'DeepSeek', 'DeepSeek'
    DOUBAO = 'DouBao', '字节豆包'
    HUNYUAN = 'HunYuan', '腾讯混元'
    SILICON_FLOW = 'SiliconFlow', '硅基流动'
    ZHIPU = 'ZhiPu', '智谱'
    MINIMAX = 'MiniMax', 'MiniMax'
    MOONSHOT = 'Moonshot', '月之暗灭'
    BAICHUAN = 'BaiChuan', '百川智能'