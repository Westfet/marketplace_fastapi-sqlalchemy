import random
import json
import logging
from sqlalchemy.future import select
from models.order import Order, OrderStatus
from pydantic import BaseModel
from fastapi import HTTPException
from typing import List
from rabbit.rabbitmq import rabbitmq
from sqlalchemy.exc import SQLAlchemyError
from queries.database import get_db

logger = logging.getLogger(__name__)


class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str


async def rabbitmq_order_worker(order: OrderCreate):
    order_data = json.dumps(order.dict())
    logger.info("... Start processing order ...")
    await rabbitmq.send_message('order_creating', order_data)


async def create_order(message_body: str):
    order_data = json.loads(message_body)

    async for session in get_db():
        try:
            new_order = Order(user_id=order_data["user_id"], status=OrderStatus.in_process)
            session.add(new_order)
            await session.commit()
            await rabbitmq.send_message('order_processing', f"Order {new_order.id} created and sent for processing!")
        except SQLAlchemyError:
            await session.rollback()


async def process_new_order(message_body: str):
    logger.info("... Check necessary details ...")
    random_number = random.randint(1, 2)
    await rabbitmq.send_message('order_notifications', str(random_number))


async def notify_customer(message_body: str):
    logger.info("... Notify customer ...")
    answer = int(message_body)
    if answer == 2:
        logger.info("Order processed successfully!")
    else:
        logger.info("Order could not be processed.")


async def get_order(order_id: int):
    async for session in get_db():
        try:
            result = await session.execute(select(Order).filter(Order.id == order_id))
            db_order = result.scalars().first()
            if db_order is None:
                raise HTTPException(status_code=404, detail="Order not found")
            return db_order
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
