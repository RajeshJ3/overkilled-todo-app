from abc import abstractmethod


class MessageBrokerFactory:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def json(self, *args, **kwargs) -> dict:
        pass
