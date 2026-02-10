from abc import ABC, abstractmethod


class ChatAdapter(ABC):

    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass