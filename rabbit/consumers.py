from rabbit.rabbitmq import rabbitmq
from controllers.orders_controller import create_order, process_new_order, notify_customer


async def start_consumers():
    await rabbitmq.consume_messages('order_creating', create_order)
    await rabbitmq.consume_messages('order_processing', process_new_order)
    await rabbitmq.consume_messages('order_notifications', notify_customer)
