from rabbit.rabbitmq import rabbitmq
from controllers.orders_controller import create_order, process_new_order, notify_customer
from asyncio import create_task


async def start_consumers():
    create_task(rabbitmq.consume_messages('order_creating', create_order))
    create_task(rabbitmq.consume_messages('order_processing', process_new_order))
    create_task(rabbitmq.consume_messages('order_notifications', notify_customer))
