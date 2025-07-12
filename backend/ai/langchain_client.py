from langchain.schema import HumanMessage

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_community.chat_models import ChatOpenAI


class MyHandler(AsyncCallbackHandler):
    def __init__(self, send_func):
        super().__init__()
        self.send_func = send_func

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.send_func(token)

async def get_ai_reply_stream(message: str, send_func, api_key, api_base, model_name):
    # 实例化时就带回调
    chat = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base=api_base,
        model_name=model_name,
        temperature=0.7,
        streaming=True,
        callbacks=[MyHandler(send_func)]
    )
    await chat.ainvoke([HumanMessage(content=message)])