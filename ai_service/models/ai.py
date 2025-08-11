from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
)
from sqlalchemy.orm import relationship, declarative_base

from db.session import Base
from models.base import CoreModel
from models.user import DjangoUser  # 确保导入 DjangoUser
from llm.enums import LLMProvider

# 状态选择类（示例）
class CommonStatus:
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def choices():
        return [(0, '禁用'), (1, '启用')]


# 平台选择类（示例）
class PlatformChoices:
    OPENAI = LLMProvider.OPENAI
    ALIMNS = 'alimns'

    @staticmethod
    def choices():
        return [(LLMProvider.OPENAI, 'OpenAI'), ('alimns', '阿里云MNS')]


# 消息类型选择类（示例）
class MessageType:
    SYSTEM = "system"  # 系统指令
    USER = "user"  # 用户消息
    ASSISTANT = "assistant"  # 助手回复
    FUNCTION = "function"  # 函数返回结果

    @staticmethod
    def choices():
        """返回可用的消息角色选项"""
        return [
            (MessageType.SYSTEM, "系统"),
            (MessageType.USER, "用户"),
            (MessageType.ASSISTANT, "助手"),
            (MessageType.FUNCTION, "函数")
        ]


class MessageContentType:
    """消息内容类型"""
    TEXT = "text"
    FUNCTION_CALL = "function_call"

    @staticmethod
    def choices():
        """返回可用的内容类型选项"""
        return [
            (MessageContentType.TEXT, "文本"),
            (MessageContentType.FUNCTION_CALL, "函数调用")
        ]

# AI API 密钥表
class AIApiKey(CoreModel):
    __tablename__ = 'ai_api_key'

    name = Column(String(255), nullable=False)
    platform = Column(String(100), nullable=False)
    api_key = Column(String(255), nullable=False)
    url = Column(String(255), nullable=True)
    status = Column(Integer, default=CommonStatus.DISABLED)

    def __str__(self):
        return self.name


# AI 模型表
class AIModel(CoreModel):
    __tablename__ = 'ai_model'

    name = Column(String(64), nullable=False)
    sort = Column(Integer, default=0)
    status = Column(Integer, default=CommonStatus.DISABLED)
    key_id = Column(Integer, ForeignKey('ai_api_key.id'), nullable=False)
    model_type = Column(String(32), nullable=True)
    platform = Column(String(32), nullable=False)
    model = Column(String(64), nullable=False)
    temperature = Column(Float, nullable=True)
    max_tokens = Column(Integer, nullable=True)
    max_contexts = Column(Integer, nullable=True)

    key = relationship('AIApiKey', backref='models')

    def __str__(self):
        return self.name


# AI 工具表
class Tool(CoreModel):
    __tablename__ = 'ai_tool'

    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    status = Column(Integer, default=0)

    def __str__(self):
        return self.name


# AI 知识库表
class Knowledge(CoreModel):
    __tablename__ = 'ai_knowledge'

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    embedding_model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=False)
    embedding_model = Column(String(32), nullable=False)
    top_k = Column(Integer, default=0)
    similarity_threshold = Column(Float, nullable=False)
    status = Column(Integer, default=CommonStatus.DISABLED)

    embedding_model_rel = relationship('AIModel', backref='knowledges')
    documents = relationship('KnowledgeDocument', backref='knowledge', cascade='all, delete-orphan')
    segments = relationship('KnowledgeSegment', backref='knowledge', cascade='all, delete-orphan')
    roles = relationship('ChatRole', secondary='ai_chat_role_knowledge', backref='knowledges')

    def __str__(self):
        return self.name


# AI 知识库文档表
class KnowledgeDocument(CoreModel):
    __tablename__ = 'ai_knowledge_document'

    knowledge_id = Column(Integer, ForeignKey('ai_knowledge.id'), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(1024), nullable=False)
    content = Column(Text, nullable=False)
    content_length = Column(Integer, nullable=False)
    tokens = Column(Integer, nullable=False)
    segment_max_tokens = Column(Integer, nullable=False)
    retrieval_count = Column(Integer, default=0)
    status = Column(Integer, default=CommonStatus.DISABLED)

    segments = relationship('KnowledgeSegment', backref='document', cascade='all, delete-orphan')

    def __str__(self):
        return self.name


# AI 知识库分段表
class KnowledgeSegment(CoreModel):
    __tablename__ = 'ai_knowledge_segment'

    knowledge_id = Column(Integer, ForeignKey('ai_knowledge.id'), nullable=False)
    document_id = Column(Integer, ForeignKey('ai_knowledge_document.id'), nullable=False)
    content = Column(Text, nullable=False)
    content_length = Column(Integer, nullable=False)
    tokens = Column(Integer, nullable=False)
    vector_id = Column(String(100), nullable=True)
    retrieval_count = Column(Integer, default=0)
    status = Column(Integer, default=CommonStatus.DISABLED)

    def __str__(self):
        return f"Segment {self.id}"


# AI 聊天角色表
class ChatRole(CoreModel):
    __tablename__ = 'ai_chat_role'

    name = Column(String(128), nullable=False)
    avatar = Column(String(256), nullable=False)
    description = Column(String(256), nullable=True)
    status = Column(Integer, default=CommonStatus.DISABLED)
    sort = Column(Integer, default=0)
    public_status = Column(Boolean, default=False)
    category = Column(String(32), nullable=True)
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=False)
    system_message = Column(String(1024), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey('system_users.id'),  # 假设DjangoUser表名是system_users
        nullable=True  # 允许为空（如匿名角色）
    )
    user = relationship(DjangoUser, backref='chat_roles')  # 正确：DjangoUser 已定义并导入

    model = relationship('AIModel', backref='chat_roles')
    tools = relationship('Tool', secondary='ai_chat_role_tool', backref='roles')
    # conversations = relationship('ChatConversation', backref='role', cascade='all, delete-orphan')
    # messages = relationship('ChatMessage', backref='role', cascade='all, delete-orphan')

    def __str__(self):
        return self.name

# AI 聊天对话表
class ChatConversation(CoreModel):
    __tablename__ = 'ai_chat_conversation'

    title = Column(String(256), nullable=False)
    pinned = Column(Boolean, default=False)
    pinned_time = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('system_users.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('ai_chat_role.id'), nullable=True)
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=False)
    model = Column(String(32), nullable=False)
    system_message = Column(String(1024), nullable=True)
    temperature = Column(Float, nullable=False)
    max_tokens = Column(Integer, nullable=False)
    max_contexts = Column(Integer, nullable=False)
    user = relationship(DjangoUser, backref='conversations')  # 正确：DjangoUser 已定义并导入

    model_rel = relationship('AIModel', backref='conversations')
    messages = relationship('ChatMessage', backref='conversation', cascade='all, delete-orphan')

    def __str__(self):
        return self.title


# AI 聊天消息表
class ChatMessage(CoreModel):
    __tablename__ = 'ai_chat_message'

    conversation_id = Column(Integer, ForeignKey('ai_chat_conversation.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('system_users.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('ai_chat_role.id'), nullable=True)
    model = Column(String(32), nullable=False)
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=False)
    type = Column(String(16), nullable=False)
    reply_id = Column(Integer, nullable=True)
    content = Column(String(2048), nullable=False)
    use_context = Column(Boolean, default=False)
    segment_ids = Column(String(2048), nullable=True)

    user = relationship(DjangoUser, backref='messages')  # 正确：DjangoUser 已定义并导入
    model_rel = relationship('AIModel', backref='messages')

    def __str__(self):
        return self.content[:30]


# 聊天角色与知识库的关联表
class ChatRoleKnowledge(Base):
    __tablename__ = 'ai_chat_role_knowledge'

    chat_role_id = Column(Integer, ForeignKey('ai_chat_role.id'), primary_key=True)
    knowledge_id = Column(Integer, ForeignKey('ai_knowledge.id'), primary_key=True)


# 聊天角色与工具的关联表
class ChatRoleTool(Base):
    __tablename__ = 'ai_chat_role_tool'

    chat_role_id = Column(Integer, ForeignKey('ai_chat_role.id'), primary_key=True)
    tool_id = Column(Integer, ForeignKey('ai_tool.id'), primary_key=True)


class Drawing(CoreModel):
    __tablename__ = 'ai_drawing'

    user_id = Column(Integer, ForeignKey('system_users.id'), nullable=True)
    public_status = Column(Boolean, default=False, nullable=False)

    platform = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)

    prompt = Column(Text(length=2000), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    options = Column(JSON, nullable=True)

    status = Column(String(20), nullable=False)
    pic_url = Column(String(2048), nullable=True)
    error_message = Column(String(1024), nullable=True)

    task_id = Column(String(1024), nullable=True)
    buttons = Column(String(2048), nullable=True)

    user = relationship("DjangoUser", backref="images")

    def __str__(self):
        return f"Image #{self.id} ({self.prompt[:30]})"