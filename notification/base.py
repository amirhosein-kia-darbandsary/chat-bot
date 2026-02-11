from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, text: str, destination: str):
        pass
