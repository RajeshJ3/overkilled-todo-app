from os import environ as env
import logging

# libs
from events_framework.publisher.event_publisher import EventPublisher
from events_framework.publisher.brokers.rabbitmq import RabbitMQPublisher
from events_framework.subscriber.event_subscriber import EventSubscriber
from events_framework.subscriber.brokers.rabbitmq import RabbitMQSubscriber
from events_framework.utils.queues import Queue


async def publish_to_rabbitmq_queue(data: dict, queue: Queue) -> None:
    broker = RabbitMQPublisher(
        host=env["RABBITMQ_HOST"],
        port=env.get("RABBITMQ_PORT", "5672"),
        username=env["RABBITMQ_USERNAME"],
        password=env["RABBITMQ_PASSWORD"],
        queue_name=queue.value,
        virtual_host=env.get("RABBITMQ_VIRTUAL_HOST", "/"),
    )
    publisher = EventPublisher(broker)

    await publisher.publish(data)

    action = data.get("action")
    logging.info(
        f"[MESSAGE_PUBLIHSHED ✅] to rabbitmq queue: {queue.value} (event: {action})"
    )


async def consume_from_rabbitmq_queue(queue: Queue, callback) -> None:
    broker = RabbitMQSubscriber(
        host=env["RABBITMQ_HOST"],
        port=env.get("RABBITMQ_PORT", "5672"),
        username=env["RABBITMQ_USERNAME"],
        password=env["RABBITMQ_PASSWORD"],
        queue_name=queue.value,
        virtual_host=env.get("RABBITMQ_VIRTUAL_HOST", "/"),
    )
    subscriber = EventSubscriber(broker)

    await subscriber.get_messages(callback)
