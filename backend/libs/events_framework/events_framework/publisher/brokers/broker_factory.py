from abc import abstractmethod


class PublisherBrokerFactory:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def publish(self, data: dict, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def close_connection(self, *args, **kwargs) -> None:
        pass
