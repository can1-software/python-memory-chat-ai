from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Chat, Message, User
from app.services import gemini_service


def get_user_chat(db: Session, user: User, chat_id: int) -> Chat:
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id, Chat.user_id == user.id)
        .first()
    )
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    return chat


def create_chat(db: Session, user: User, title: str) -> Chat:
    chat = Chat(user_id=user.id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def list_user_chats(db: Session, user: User) -> list[Chat]:
    return (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.updated_at.desc())
        .all()
    )


def add_message(
    db: Session,
    user: User,
    chat_id: int,
    content: str,
    role: str = "user",
) -> Message:
    chat = get_user_chat(db, user, chat_id)

    message = Message(chat_id=chat.id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_recent_messages(db: Session, chat_id: int, limit: int = 10) -> list[Message]:
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    messages.reverse()
    return messages


def send_message_with_ai(
    db: Session,
    user: User,
    chat_id: int,
    content: str,
) -> dict:
    chat = get_user_chat(db, user, chat_id)

    user_message = Message(chat_id=chat.id, role="user", content=content)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    recent_messages = get_recent_messages(db, chat.id, limit=10)
    history = [{"role": message.role, "content": message.content} for message in recent_messages]

    try:
        assistant_content = gemini_service.generate_response(history)
    except gemini_service.GeminiServiceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service is temporarily unavailable. Your message was saved.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service is temporarily unavailable. Your message was saved.",
        )

    assistant_message = Message(
        chat_id=chat.id,
        role="assistant",
        content=assistant_content,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {
        "user_message": user_message,
        "assistant_message": assistant_message,
    }
