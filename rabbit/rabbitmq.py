import aio_pika
import logging
from aio_pika import Message, DeliveryMode
from typing import Callable, Optional
from rabbit.rabbit_config import RABBITMQ_URL

logger = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(self, url: str):
        self.url = url
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.Channel] = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
        except Exception as e:
            print(f"Failed to connect or initialize channel: {e}")
            self.connection = None
            self.channel = None
            raise

    async def declare_queue(self, queue_name: str):
        if not self.channel:
            raise RuntimeError("Channel is not initialized. Call connect() first.")
        return await self.channel.declare_queue(queue_name, durable=True)

    async def send_message(self, queue_name: str, message: str):
        if not self.channel:
            raise RuntimeError("Channel is not initialized. Call connect() first.")
        await self.declare_queue(queue_name)
        await self.channel.default_exchange.publish(
            Message(
                message.encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name
        )

    async def consume_messages(self, queue_name: str, callback: Callable):
        if not self.channel:
            raise RuntimeError("Channel is not initialized. Call connect() first.")
        queue = await self.declare_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    logger.info(f"Received message: {message.body.decode()}")
                    async with message.process():
                        await callback(message.body.decode())
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None


# Экземпляр класса RabbitMQ
rabbitmq = RabbitMQ(RABBITMQ_URL)
