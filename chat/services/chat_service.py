# LangChain集成示例
from sqlalchemy.orm import Session
from datetime import datetime
from models.ai import ChatConversation, ChatMessage, MessageType

class ChatDBService:
    @staticmethod
    def get_or_create_conversation(db: Session, conversation_id: int | None, user_id: int, model: str, content: str) -> ChatConversation:
        if not conversation_id:
            print(conversation_id, 'conversation_id')
            conversation = ChatConversation(
                title=content,
                user_id=user_id,
                role_id=None,
                model_id=None,  # 需根据实际模型id调整
                model=model,
                system_message=None,
                temperature=0.7,
                max_tokens=2048,
                max_contexts=10,
                create_time=datetime.now(),
                update_time=datetime.now(),
                is_deleted=False
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            return conversation
        else:
            conversation = db.query(ChatConversation).get(conversation_id)
            if not conversation:
                raise ValueError("无效的conversation_id")
            return conversation

    @staticmethod
    def add_message(db: Session, conversation: ChatConversation, user_id: int, content: str) -> ChatMessage:
        message = ChatMessage(
            conversation_id=conversation.id,
            user_id=user_id,
            role_id=None,
            model=conversation.model,
            model_id=conversation.model_id,
            type=MessageType.USER,
            reply_id=None,
            content=content,
            use_context=True,
            segment_ids=None,
            create_time=datetime.now(),
            update_time=datetime.now(),
            is_deleted=False
        )
        db.add(message)
        db.commit()
        return message

    @staticmethod
    def insert_ai_message(db: Session, conversation, user_id: int, content: str, model: str):
        from datetime import datetime
        from models.ai import MessageType
        message = ChatMessage(
            conversation_id=conversation.id,
            user_id=user_id,
            role_id=None,
            model=model,
            model_id=conversation.model_id,
            type=MessageType.ASSISTANT,
            reply_id=None,
            content=content,
            use_context=True,
            segment_ids=None,
            create_time=datetime.now(),
            update_time=datetime.now(),
            is_deleted=False
        )
        db.add(message)
        db.commit()

    @staticmethod
    def get_history(db: Session, conversation_id: int) -> list[ChatMessage]:
        return db.query(ChatMessage).filter_by(conversation_id=conversation_id).order_by(ChatMessage.id).all()

