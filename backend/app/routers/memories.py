from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import User
from app.schemas import MemoryCreate, MemoryDeleteResponse, MemoryResponse
from app.services import memory_service

router = APIRouter(prefix="/memories", tags=["memories"])


@router.get("", response_model=list[MemoryResponse])
def list_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return memory_service.list_user_memories(db, current_user)


@router.post("", response_model=MemoryResponse, status_code=201)
def create_or_update_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return memory_service.upsert_memory(
        db,
        current_user,
        memory_data.key,
        memory_data.value,
    )


@router.delete("/{memory_id}", response_model=MemoryDeleteResponse)
def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory_service.delete_user_memory(db, current_user, memory_id)
    return MemoryDeleteResponse(message="Memory deleted successfully")
