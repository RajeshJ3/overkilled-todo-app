import json

from pika import BlockingConnection, ConnectionParameters, credentials

from events_framework.publisher.brokers.broker_factory import PublisherBrokerFactory


class RabbitMQPublisher(PublisherBrokerFactory):
    def __init__(
        self,
        host: str,
        port: str,
        username: str,
        password: str,
        queue_name: str,
        virtual_host: str = "/",
        routing_key: str = None,
        exchange: str = "",
    ):

        self.queue_name = queue_name
        self.routing_key = routing_key or self.queue_name
        self.exchange = exchange

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

    async def publish(self, data: dict) -> None:
        str_data = json.dumps(data).encode("utf-8")
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=self.routing_key, body=str_data
        )

    async def close_connection(self) -> None:
        self.connection.close()
