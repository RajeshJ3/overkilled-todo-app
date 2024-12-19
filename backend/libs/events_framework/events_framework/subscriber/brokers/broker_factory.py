from abc import abstractmethod
from events_framework.message.brokers.broker_factory import MessageBrokerFactory


class SubscriberBrokerFactory:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_one_message(self, *args, **kwargs) -> MessageBrokerFactory:
        pass

    @abstractmethod
    async def get_messages(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def consume_messages(self, *args, **kwargs) -> MessageBrokerFactory:
        pass

    @abstractmethod
    async def ack_message(self, message: MessageBrokerFactory) -> None:
        pass

    @abstractmethod
    async def ack_messages(self, messages: list[MessageBrokerFactory]) -> None:
        pass
