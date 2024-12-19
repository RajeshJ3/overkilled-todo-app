import asyncio
import logging

from sqlalchemy.orm.session import Session

from events_framework.message.brokers.rabbitmq import RabbitMQMessage
from events_framework.utils.rabbitmq_utils import consume_from_rabbitmq_queue

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from teams_context.db.connection import db_dependency
from teams_context.utils.events.queues import Queue
from teams_context.event_consumer_svc.event_handlers.handlers import HANDLERS


def message_handler(
    ch: BlockingChannel, method: Basic, _: BasicProperties, body: bytes, db: Session
):
    message = RabbitMQMessage(method, body)
    message_data = message.json()
    event_type = message_data.get("action", None)

    if not event_type:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    event_handler = HANDLERS.get(event_type)
    if not event_handler:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        success = event_handler(message_data, db)
        if success:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        logging.info(f"Unsuccessful message handling for event {event_type}")

    except:
        logging.error(f"Error while handling message for event {event_type}")


def message_handler_wrapper(db: Session):
    def exec(*args, **kwargs):
        message_handler(*args, **kwargs, db=db)

    return exec


async def main():
    db: Session = next(db_dependency())
    await consume_from_rabbitmq_queue(
        queue=Queue.USERS, callback=message_handler_wrapper(db)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
    loop.close()
