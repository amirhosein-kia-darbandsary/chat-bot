from telethon import TelegramClient, events
import asyncio
from prompts import WORK_STATUS_PROMPTS
from dotenv import load_dotenv
import os
from chat.ask_gpt import OpenAIAdapter
from chat.facade import ChatService
from handler.checkers import pending_emergency, check_rate_limit
from handler.message_handlers import (
    cancel_emergency,
    process_message,
    handle_emergency,
    find_resume_file,
)
from handler.get_status import get_work_status


# ================= CONFIG =================
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION", "amir0903")
api_key_host = os.getenv("OPEN_API_KEY")

RESUME_PATH_DIR = os.getenv("RESUME_PATH", "./static")
resume_path = find_resume_file(RESUME_PATH_DIR)

client = TelegramClient(session_name, api_id, api_hash)
assistent = ChatService(OpenAIAdapter(api_key=api_key_host))


# ---------------------------
# هندلر اصلی
# ---------------------------
@client.on(events.NewMessage(incoming=True))
async def handler(event):

    # فقط چت خصوصی
    if not event.is_private:
        return

    # اگر free هستی → ربات ساکت
    work_status = get_work_status()
    if work_status == "free":
        return

    sender = await event.get_sender()
    user_id = sender.id

    text = (event.raw_text or "").strip()
    if not text:
        return

    # ---------------------------
    # Rate limit
    # ---------------------------
    allowed, count = check_rate_limit(user_id, text)

    if not allowed:
        return

    # ---------------------------
    # حالت انتظار برای انتخاب کاربر
    # ---------------------------
    if user_id in pending_emergency:

        # ---------- EMERGENCY ----------
        if text in ("1", "۱"):
            await handle_emergency(user_id, sender, event, text)

        # ---------- SEND RESUME ----------
        elif text in ("2", "۲"):
            if os.path.exists(str(resume_path)):
                await event.reply("رزومه برای شما ارسال شد.")
                await event.reply(file=resume_path)
            else:
                await event.reply("متأسفانه فایل رزومه در دسترس نیست.")

            pending_emergency.pop(user_id, None)

        # ---------- CANCEL ----------
        else:
            await cancel_emergency(user_id, sender, event)
            status_prompt = WORK_STATUS_PROMPTS.get(work_status, "")

            await process_message(
                event=event,
                text=text,
                status_prompt=status_prompt,
                assistent=assistent,
                number_of_ask=count
            )

        return

    # ---------------------------
    # پاسخ عادی
    # ---------------------------
    status_prompt = WORK_STATUS_PROMPTS.get(work_status, "")

    await process_message(
        event=event,
        text=text,
        status_prompt=status_prompt,
        assistent=assistent,
        number_of_ask=count
    )


# ---------------------------
# اجرای ربات
# ---------------------------
async def main():
    await client.start()
    print("Telegram auto-reply is running...")
    await client.run_until_disconnected()


asyncio.run(main())
