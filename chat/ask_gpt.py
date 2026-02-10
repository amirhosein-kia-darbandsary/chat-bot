from openai import OpenAI
from chat.base import ChatAdapter

class OpenAIAdapter(ChatAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "تو یک دستیار حرفه‌ای هستی که پاسخ‌ها را "
                        "کوتاه، دقیق و متناسب با وضعیت کاری کاربر می‌نویسی."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
