from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.user_controller import UserCreate, create_user, get_user
from queries.database import get_db

router = APIRouter()


@router.post("/", response_model=UserCreate)
def create_user_view(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.get("/{user_id}", response_model=UserCreate)
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)
