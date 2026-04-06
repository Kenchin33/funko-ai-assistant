from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageRead,
    ChatSessionCreate,
    ChatSessionRead,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat")


@router.post("/sessions", response_model=ChatSessionRead, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    payload: ChatSessionCreate,
    db: Session = Depends(get_db),
):
    return ChatService.create_session(db, payload)


@router.get("/sessions/{session_id}", response_model=ChatSessionRead)
def get_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    session = ChatService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )
    return session


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_message(
    session_id: int,
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
):
    session = ChatService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return ChatService.create_message(db, session_id, payload)


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageRead])
def get_chat_messages(
    session_id: int,
    db: Session = Depends(get_db),
):
    session = ChatService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return ChatService.get_messages_by_session_id(db, session_id)