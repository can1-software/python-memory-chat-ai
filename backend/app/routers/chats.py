from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import User
from app.schemas import (
    ChatCreate,
    ChatDetailResponse,
    ChatListItem,
    ChatResponse,
    MessageCreate,
    MessageExchangeResponse,
)
from app.services import chat_service

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=ChatResponse, status_code=201)
def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.create_chat(db, current_user, chat_data.title)


@router.get("", response_model=list[ChatListItem])
def list_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.list_user_chats(db, current_user)


@router.get("/{chat_id}", response_model=ChatDetailResponse)
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.get_user_chat(db, current_user, chat_id)


@router.post("/{chat_id}/messages", response_model=MessageExchangeResponse, status_code=201)
def send_message(
    chat_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.send_message_with_ai(
        db,
        current_user,
        chat_id,
        message_data.content,
    )
