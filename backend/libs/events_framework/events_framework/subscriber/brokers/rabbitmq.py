import logging

from pika import BlockingConnection, ConnectionParameters, credentials
from pika.spec import Basic

from events_framework.subscriber.brokers.broker_factory import (
    SubscriberBrokerFactory,
)
from events_framework.message.brokers.rabbitmq import RabbitMQMessage


class RabbitMQSubscriber(SubscriberBrokerFactory):
    def __init__(
        self,
        host: str,
        port: str,
        username: str,
        password: str,
        queue_name: str,
        virtual_host: str = "/",
    ):

        self.queue_name = queue_name

        self.connection = BlockingConnection(
            ConnectionParameters(
                host=host,
                port=port,
                virtual_host=virtual_host,
                credentials=credentials.PlainCredentials(username, password),
            )
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=queue_name)

    async def get_one_message(self) -> RabbitMQMessage:

        status, _, data = self.channel.basic_get(queue=self.queue_name, auto_ack=False)

        if type(status) != Basic.GetOk:
            logging.info("No message received.")
            return

        status: Basic.GetOk

        return RabbitMQMessage(status, data)

    async def get_messages(self, callback) -> None:

        try:
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=callback, auto_ack=False
            )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logging.info("Stopping consuming messages!")
        finally:
            self.connection.close()

    async def ack_message(self, message: RabbitMQMessage) -> None:
        self.channel.basic_ack(message.status.delivery_tag)

    async def ack_messages(self, messages: list[RabbitMQMessage]) -> None:
        for message in messages:
            self.ack_message(message)
