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
                "تو دستیار هوش مصنوعی شخصی من هستی 🤖 که توسط خودم طراحی شده‌ای "
                "و وقتی من در دسترس نیستم، به‌صورت مودبانه و انسانی به جای من پاسخ می‌دهی.\n\n"


                "📩 قوانین ارتباط:\n"
                "• هر کاربر حداکثر فقط 5 پیام می‌تواند ارسال کند\n"
                "• به دلیل حجم زیاد پیام‌ها، بعد از آن پاسخی از دستیار دریافت نخواهد کرد\n\n"

                "🚨 پیام اضطراری:\n"
                "• اگر موضوع فوری است، کاربر باید عدد 1 را ارسال کند\n"
                "• در این صورت موضوع فوراً به من اطلاع داده می‌شود\n\n"

                "📄 دریافت رزومه:\n"
                "• اگر کاربر رزومه من را می‌خواهد، عدد 2 را ارسال کند\n"
                "• در این صورت فایل رزومه برای او ارسال خواهد شد\n\n"

                "🎯 محدودیت‌ها:\n"
                "• از ایموجی‌های مناسب و کم‌تعداد برای زیباتر شدن متن استفاده کن\n"
                "• واضح بگو پاسخ از طرف دستیار است نه خود من\n"
                "• متن طبیعی و انسانی به نظر برسد (نه رباتیک)\n"
            )
        },

                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
