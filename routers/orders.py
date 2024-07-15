from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.order_controller import OrderCreate, create_order, get_order
from queries.database import get_db

router = APIRouter()


@router.post("/", response_model=OrderCreate)
def create_order_view(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(order, db)


@router.get("/{order_id}", response_model=OrderCreate)
def get_order_view(order_id: int, db: Session = Depends(get_db)):
    return get_order(order_id, db)
