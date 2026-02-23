from handler.checkers import pending_emergency, DAILY_LIMIT
import os
from notification.sms import SmsNotification
from datetime import datetime


async def handle_emergency(user_id, sender,event, text):
    original_text = pending_emergency[user_id]["original_text"]

    sms = SmsNotification(
        username=os.environ.get('USERNAME_SMS'),
        default_from="50002710064873",
        password=os.environ.get("SMS_API_KEY")
    )

    result = sms.send(
        text=f"EMERGENCY from {sender.first_name}:\n{original_text}",
        destination="09038184873"
    )
    print(result)
    await event.reply(
        "پیام شما به عنوان مورد اضطراری ثبت شد و اطلاع‌رسانی انجام گردید."
    )
    pending_emergency.pop(user_id, None)


async def cancel_emergency(user_id, sender, event):
    pending_emergency.pop(user_id, None)

async def process_message(
    event,
    text,
    status_prompt,
    assistent,
    number_of_ask: int = 0
):
    """ارسال پاسخ با رفتار متفاوت برای پیام اول و پیام‌های بعدی"""

    # =========================
    # 🥇 FIRST MESSAGE
    # =========================
    print(number_of_ask)
    if number_of_ask in (0,1):

        final_prompt = f"""
        ─────────────────────────────
        📌 شرح وضعیت فعلی من:
        {status_prompt}

        در حال حاضر شخصاً در دسترس نیستم
        و این پیام توسط دستیار من ارسال شده است.
        اگر سوالی دارید بپرسید حتما جواب خواهم داد.
        • هر کاربر حداکثر 5 پاسخ در ۲۴ ساعت دریافت می‌کند  
        • پس از آن پاسخ خودکار متوقف می‌شود  
        🚨 اگر موضوع اضطراری است → عدد 1 را ارسال کنید  
        📄 اگر رزومه را نیاز دارید → عدد 2 را ارسال کنید  
        قوانین رو کامل برای کاربر شرح بده 
        "اگر نیاز به معرفی بیشتر من بود یا درباره کد و برنامه نویسی من پرسیدن لینک گیت هابم رو بهشون بده : 'https://github.com/amirhosein-kia-darbandsary' "


        ─────────────────────────────
        💬 پیام کاربر:
        "{text}"

        ─────────────────────────────
        محترمانه و انسانی بنویس.
        """

    # =========================
    # 🥈 FOLLOW-UP MESSAGES
    # =========================
    else:

        final_prompt = f"""
        تو به جای من و به عنوان دستیار پاسخ می‌دهی.

        در صورت نیاز برای جواب سوال کاربر اگر نیاز است که در منابع بگردی انجام بده
        سوال کاربر رو کامل جواب ده
        اگر نیاز داشتی که جواب کاربر رو با نمودار  و جدول توضیح بدی در قالب markdown  بدی که بشه روی پیام تلگرام به صورت زیبا نشان داد
        پیام:
        "{text}"
        """

    # =========================
    # 🤖 Generate Reply
    # =========================
    assistant_reply = assistent.adapter.complete(final_prompt)

    await event.reply(assistant_reply)

    pending_emergency[event.sender_id] = {
        "original_text": text,
        "timestamp": datetime.now()
    }


def find_resume_file(directory: str) -> str | None:
    for root, _, files in os.walk(directory):
        print(directory)
        print(os.walk(directory))
        for file in files:
            if file.lower().endswith(".pdf"):
                return os.path.join(root, file)
    return None