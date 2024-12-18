from events_framework.subscriber.brokers.broker_factory import (
    SubscriberBrokerFactory,
)
from events_framework.message.brokers.broker_factory import MessageBrokerFactory


class EventSubscriber:

    def __init__(self, broker: SubscriberBrokerFactory):
        self.broker = broker
        pass

    async def get_one_message(self) -> MessageBrokerFactory:
        return await self.broker.get_one_message()

    async def ack_message(self, message: MessageBrokerFactory) -> None:
        return await self.broker.ack_message(message)

    async def ack_messages(self, messages: list[MessageBrokerFactory]) -> None:
        return await self.broker.ack_messages(messages)
