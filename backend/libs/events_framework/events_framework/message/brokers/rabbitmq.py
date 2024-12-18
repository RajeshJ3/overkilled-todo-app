import json

from pika.spec import Basic

from events_framework.message.brokers.broker_factory import MessageBrokerFactory


class RabbitMQMessage(MessageBrokerFactory):
    def __init__(self, status: Basic.GetOk, data: bytes):
        self.status = status
        self.data = data

    def json(self) -> dict:
        return json.loads(self.data.decode("utf-8"))
