import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.orders_controller import OrderCreate, get_order, OrderResponse
from queries.database import get_db
from rabbit.rabbitmq import rabbitmq

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order_view(order: OrderCreate):
    # Преобразование данных в JSON и отправка в очередь
    order_data = json.dumps(order.dict())
    await rabbitmq.send_message('order_creating', order_data)

    return {"message": "... Заказ создается..."}


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_view(order_id: int, db: Session = Depends(get_db)):
    return await get_order(order_id, db)
