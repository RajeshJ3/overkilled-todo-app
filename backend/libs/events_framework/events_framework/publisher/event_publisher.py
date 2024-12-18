from events_framework.publisher.brokers.broker_factory import PublisherBrokerFactory


class EventPublisher:

    def __init__(self, broker: PublisherBrokerFactory):
        self.broker = broker
        pass

    async def publish(self, data: dict) -> bool:
        return await self.broker.publish(data)

    async def close_connection(self) -> None:
        return await self.broker.close_connection()
