import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Memory, User

SENSITIVE_KEYWORDS = (
    "sağlık",
    "hastalık",
    "din",
    "siyasi",
    "politik",
    "cinsel",
    "şifre",
    "password",
)


def _clean_value(value: str) -> str:
    return value.strip().strip(".,!?;:")


def _is_sensitive(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in SENSITIVE_KEYWORDS)


def extract_memories_from_message(content: str) -> list[dict]:
    """Extract memories only from explicit, safe user phrases."""
    if _is_sensitive(content):
        return []

    extracted: list[dict] = []
    seen_keys: set[str] = set()

    patterns = [
        (re.compile(r"(?i)benim ad[ıi]m\s+([^.,!?;]+)"), "name"),
        (re.compile(r"(?i)ad[ıi]m\s+([^.,!?;]+)"), "name"),
        (re.compile(r"(?i)bunu hatırla:\s*(.+)"), "note"),
    ]

    for pattern, key in patterns:
        match = pattern.search(content)
        if match:
            value = _clean_value(match.group(1))
            if value and key not in seen_keys:
                extracted.append({"key": key, "value": value})
                seen_keys.add(key)

    if re.search(r"(?i)bana k[ıi]sa cevap ver", content) and "response_style" not in seen_keys:
        extracted.append({"key": "response_style", "value": "kısa cevap"})

    return extracted


def format_memories_for_prompt(memories: list[Memory]) -> str:
    if not memories:
        return ""

    lines = ["User memories:"]
    for memory in memories:
        lines.append(f"- {memory.key}: {memory.value}")

    lines.append(
        "Use this information when answering, but do not repeat it unnecessarily "
        "unless the user explicitly asks."
    )
    return "\n".join(lines)


def list_user_memories(db: Session, user: User) -> list[Memory]:
    return (
        db.query(Memory)
        .filter(Memory.user_id == user.id)
        .order_by(Memory.updated_at.desc())
        .all()
    )


def upsert_memory(
    db: Session,
    user: User,
    key: str,
    value: str,
    source_message_id: int | None = None,
) -> Memory:
    memory = (
        db.query(Memory)
        .filter(Memory.user_id == user.id, Memory.key == key)
        .first()
    )

    if memory:
        memory.value = value
        memory.source_message_id = source_message_id
    else:
        memory = Memory(
            user_id=user.id,
            key=key,
            value=value,
            source_message_id=source_message_id,
        )
        db.add(memory)

    db.commit()
    db.refresh(memory)
    return memory


def save_extracted_memories(
    db: Session,
    user: User,
    content: str,
    source_message_id: int | None = None,
) -> list[Memory]:
    saved: list[Memory] = []
    for item in extract_memories_from_message(content):
        memory = upsert_memory(
            db,
            user,
            item["key"],
            item["value"],
            source_message_id=source_message_id,
        )
        saved.append(memory)
    return saved


def delete_user_memory(db: Session, user: User, memory_id: int) -> None:
    memory = (
        db.query(Memory)
        .filter(Memory.id == memory_id, Memory.user_id == user.id)
        .first()
    )
    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    db.delete(memory)
    db.commit()
