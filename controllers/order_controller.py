from sqlalchemy.orm import Session
from models.order import Order, OrderStatus
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException


class OrderCreate(BaseModel):
    status: OrderStatus
    created_at: datetime
    user_id: int


def create_order(order: OrderCreate, db: Session):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_order(order_id: int, db: Session):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
