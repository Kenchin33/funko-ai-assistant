import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.schemas.chat import ChatMessageCreate, ChatSessionCreate


class ChatService:
    @staticmethod
    def create_session(db: Session, payload: ChatSessionCreate) -> ChatSession:
        session = ChatSession(
            session_token=secrets.token_urlsafe(32),
            user_name=payload.user_name,
            user_email=payload.user_email,
            source=payload.source,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> ChatSession | None:
        stmt = select(ChatSession).where(ChatSession.id == session_id)
        return db.scalar(stmt)

    @staticmethod
    def get_session_by_token(db: Session, session_token: str) -> ChatSession | None:
        stmt = select(ChatSession).where(ChatSession.session_token == session_token)
        return db.scalar(stmt)

    @staticmethod
    def create_message(
        db: Session,
        session_id: int,
        payload: ChatMessageCreate,
    ) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=payload.role,
            message_text=payload.message_text,
            detected_intent=payload.detected_intent,
            metadata_json=payload.metadata_json,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_messages_by_session_id(db: Session, session_id: int) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        )
        return list(db.scalars(stmt).all())