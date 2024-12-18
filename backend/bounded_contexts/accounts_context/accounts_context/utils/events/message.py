import logging

# libs
from events_framework.publisher.event_publisher import EventPublisher
from events_framework.publisher.brokers.rabbitmq import RabbitMQPublisher

# svc
from accounts_context import config
from accounts_context.utils.events.queues import Queue
from accounts_context.utils.events.types import EventType


def message_builder(data: dict, event_type: EventType) -> dict:
    return {
        "action": event_type.value,
        "meta": {"source_bc": config.BOUNDED_CONTEXT_NAME},
        "payload": data,
    }


async def message_publisher(data: dict, queue: Queue) -> None:
    broker = RabbitMQPublisher(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        username=config.RABBITMQ_USERNAME,
        password=config.RABBITMQ_PASSWORD,
        queue_name=queue.value,
        virtual_host=config.RABBITMQ_VIRTUAL_HOST,
    )
    publisher = EventPublisher(broker)

    await publisher.publish(data)
    logging.info(f"[Message Published]")
