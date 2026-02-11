from telethon import TelegramClient, events
import asyncio
from prompts import WORK_STATUS_PROMPTS
from dotenv import load_dotenv
import os
from chat.ask_gpt import OpenAIAdapter
from chat.facade import ChatService
from handler.checkers import pending_emergency, check_rate_limit
from handler.message_handlers import cancel_emergency, process_message, handle_emergency
from handler.get_status import get_work_status
# ================= CONFIG =================
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION", "amir0903")
api_key_host = os.getenv("OPEN_API_KEY")
WORK_STATUS = "coding"

client = TelegramClient(session_name, api_id, api_hash)
assistent = ChatService(OpenAIAdapter(api_key=api_key_host))


# ---------------------------
# هندلر اصلی
# ---------------------------
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    WORK_STATUS = get_work_status()
    if WORK_STATUS == "free":
        return
    if not event.is_private:
        return

    sender = await event.get_sender()
    user_id = sender.id
    text = event.raw_text.strip()

    if not check_rate_limit(user_id):
        await event.reply(
            "شما به محدودیت روزانه پیام رسیده‌اید. "
            "اگر پیام اضطراری باشد، اطلاع‌رسانی از طریق پیامک انجام خواهد شد."
        )
        return
    

    
    if user_id in pending_emergency:
        if text in ("1", "۱"):
            await handle_emergency(user_id, sender, event, text)
        else:
            await cancel_emergency(user_id, sender, event)
        return

    status_prompt = WORK_STATUS_PROMPTS.get(WORK_STATUS, "")
    await process_message(event, text, status_prompt, assistent)


async def main():        
    await client.start()
    print("Telegram auto-reply is running...")
    await client.run_until_disconnected()

asyncio.run(main())
