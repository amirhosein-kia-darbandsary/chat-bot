from telethon import TelegramClient, events
import requests
import asyncio
from prompts import WORK_STATUS_PROMPTS
from dotenv import load_dotenv
import os
from chat.ask_gpt import OpenAIAdapter
from chat.facade import ChatService

# ================= CONFIG =================
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION", "amir0903")
api_key_host = os.getenv("OPEN_API_KEY")
OLLAMA_MODEL = "llama3"
WORK_STATUS = "busy"


client = TelegramClient(session_name, api_id, api_hash)
assistent = ChatService(
    OpenAIAdapter(api_key=api_key_host)
)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return


    sender = await event.get_sender()
    text = event.raw_text

    status_prompt = WORK_STATUS_PROMPTS.get(WORK_STATUS, "")

    final_prompt = f"""
    تو دستیار شخصی من هستی و به‌جای من پیام می‌دهی.
    من در حال حاضر شخصاً در دسترس نیستم و این پاسخ از طرف خودِ من ارسال نشده است.

    نقش تو:
    - فقط به‌عنوان «دستیار پیام‌رسان» عمل کن
    - از بداهه‌گویی پرهیز کن
    - به هیچ سؤال فنی، شخصی یا محتوایی پاسخ نده
    - وارد بحث، توضیح، تحلیل یا راهنمایی نشو
    - صرفاً یک پاسخ کوتاه، محترمانه و اطلاع‌رسان بنویس

    وضعیت کاری فعلی من:
    {status_prompt}

    قوانین لحن:
    - کاملاً محترمانه و حرفه‌ای
    - طبیعی و انسانی
    - بدون شوخی، بدون اغراق
    - بدون اشاره به هوش مصنوعی یا سیستم خودکار

    پیام دریافتی:
    "{text}"

    اکنون فقط یک پیام کوتاه و مناسب بنویس که:
    - وضعیت فعلی را منتقل کند
    - مشخص کند پاسخ‌دهنده دستیار است نه خود من
    - از طرف مقابل انتظار یا اقدام خاصی نخواهد مگر در صورت فوریت
    """

    assistent_reply = assistent.adapter.complete(final_prompt)

    await event.reply(assistent_reply)


async def main():
    await client.start()
    print("Telegram auto-reply is running...")
    await client.run_until_disconnected()


asyncio.run(main())
