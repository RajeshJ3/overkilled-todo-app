import asyncio
import logging

from events_framework.message.brokers.rabbitmq import RabbitMQMessage
from events_framework.subscriber.event_subscriber import EventSubscriber
from events_framework.subscriber.brokers.rabbitmq import RabbitMQSubscriber

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def callback(ch: BlockingChannel, method: Basic, _: BasicProperties, body: bytes):
    message = RabbitMQMessage(method, body)
    message_data = message.json()
    print(f"{message_data=}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


async def main():
    host = "localhost"
    port = "5672"
    username = "guest"
    password = "guest"
    queue_name = "test-101"
    virtual_host = "/"

    broker = RabbitMQSubscriber(
        host=host,
        port=port,
        username=username,
        password=password,
        queue_name=queue_name,
        virtual_host=virtual_host,
    )
    subscriber = EventSubscriber(broker)

    await subscriber.get_messages(callback)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
    loop.close()
