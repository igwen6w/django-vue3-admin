# LangChain集成示例
from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class ChatService:
    def __init__(self):
        # 这里以OpenAI为例，实际可根据需要配置
        self.llm = OpenAI(temperature=0.7, api_key='sssss')

    def chat(self, prompt: str) -> str:
        # 简单调用LLM
        return self.llm(prompt)

chat_service = ChatService() 