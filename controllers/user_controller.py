from sqlalchemy.orm import Session
from models.user import User
from pydantic import BaseModel
from fastapi import HTTPException


class UserCreate(BaseModel):
    username: str
    email: str
    phone_number: str


def create_user(user: UserCreate, db: Session):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
