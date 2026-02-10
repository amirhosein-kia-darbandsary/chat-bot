from chat.base  import ChatAdapter

class ChatService:
    def __init__(self, adapter: ChatAdapter):
        self.adapter = adapter

    def reply(self, prompt: str) -> str:
        return self.adapter.complete(prompt)