import asyncio
import datetime
import logging

from uuid import uuid4

from events_framework.publisher.event_publisher import EventPublisher
from events_framework.publisher.brokers.rabbitmq import RabbitMQPublisher


async def main():
    host = "localhost"
    port = "5672"
    username = "guest"
    password = "guest"
    queue_name = "test-101"
    virtual_host = "/"

    broker = RabbitMQPublisher(host=host, port=port, username=username, password=password, queue_name=queue_name, virtual_host=virtual_host)
    publisher = EventPublisher(broker)

    for _ in range(1):
        data = {"message_id": str(uuid4()), "ts": str(datetime.datetime.now())}
        await publisher.publish(data)
        logging.info(f"[Message Published]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
    loop.close()
