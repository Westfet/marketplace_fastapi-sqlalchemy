import random
import json
from sqlalchemy.orm import Session
from models.order import Order, OrderStatus
from pydantic import BaseModel
from fastapi import HTTPException
from queries.database import session_factory
from typing import List
from rabbit.rabbitmq import rabbitmq
from sqlalchemy.exc import SQLAlchemyError


class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str


async def create_order(message_body: str):
    order_data = json.loads(message_body)
    with session_factory() as db:
        new_order = Order(user_id=order_data["user_id"], status=OrderStatus.in_process)
        db.add(new_order)
        try:
            db.commit()
            db.refresh(new_order)
            await rabbitmq.send_message('order_processing', f"Заказ {new_order.id} создан и передан на обработку!")
        except SQLAlchemyError as e:
            db.rollback()
            raise e


async def process_new_order(message_body: str):
    print(message_body)
    # Какая-то работа 1
    random_number = random.randint(1, 10)

    if random_number % 2 == 0:
        await rabbitmq.send_message('order_notifications', "2")
    else:
        await rabbitmq.send_message('order_notifications', "1")


async def notify_customer(message_body: str):
    # Какая-то работа 2
    answer = int(message_body)
    if answer == 2:
        print("заказ оформлен!")
    else:
        print("заказ не может быть оформлен((")


def get_order(order_id: int, db: Session):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


