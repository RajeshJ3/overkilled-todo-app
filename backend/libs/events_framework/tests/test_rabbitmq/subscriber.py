import asyncio
import logging

from events_framework.subscriber.event_subscriber import EventSubscriber
from events_framework.subscriber.brokers.rabbitmq import RabbitMQSubscriber


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

    message = await subscriber.get_one_message()
    if not message:
        return

    logging.info(f"[Message Received] {message.json()}")
    await subscriber.ack_message(message)
    logging.info(f"[Message Acknowledged]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
    loop.close()
