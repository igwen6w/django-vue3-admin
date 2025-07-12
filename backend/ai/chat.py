from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ai.langchain_client import get_ai_reply_stream
from ai.utils import get_first_available_ai_config


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get("message", "")

        model, api_key, api_base = await get_first_available_ai_config()

        async def send_chunk(chunk):
            await self.send(text_data=json.dumps({"is_streaming": True, "message": chunk}))

        await get_ai_reply_stream(user_message, send_chunk, model_name=model, api_key=api_key, api_base=api_base)

        # 结束标记
        await self.send(text_data=json.dumps({"done": True}))