from abc import ABC, abstractmethod


class BaseMessenger(ABC):
    @abstractmethod
    def read_messages(self):
        pass
