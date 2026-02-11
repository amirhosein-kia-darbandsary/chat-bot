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
    await event.reply("درخواست اضطراری لغو شد.")
    pending_emergency.pop(user_id, None)


async def process_message(event, text, status_prompt, assistent):
    """ارسال پاسخ معمولی از دستیار و ثبت pending emergency"""
    final_prompt = f"""
تو دستیار شخصی من هستی و به جای من پیام کوتاه و محترمانه می‌دهی.
من در حال حاضر شخصاً در دسترس نیستم و این پاسخ از طرف خود من ارسال نشده است.

وظیفه تو:
- فقط پاسخ کوتاه، محترمانه و اطلاع‌رسان بده
- وارد بحث یا مشاوره نشو
- پاسخ باید روشن کند که پیام از دستیار ارسال شده و نه خود من

وضعیت کاری فعلی من:
{status_prompt}

قوانین تعامل با کاربر:
- کاربر می‌تواند حداکثر {DAILY_LIMIT} پیام در ۲۴ ساعت با دستیار داشته باشد
- اگر پیام اضطراری است، عدد 1 را ارسال کند تا فوراً اطلاع‌رسانی انجام شود

پیام دریافتی:
"{text}"

حالا فقط یک پاسخ کوتاه و محترمانه بنویس که:
1. وضعیت فعلی من را به کاربر منتقل کند
2. مشخص کند پاسخ‌دهنده دستیار است نه خود من
3. محدودیت تعداد پیام و نحوه اعلام اضطراری را یادآوری کند
4. لحن پاسخ محترمانه و انسانی باشد
"""

    assistant_reply = assistent.adapter.complete(final_prompt)

    await event.reply(assistant_reply + "\n\nاگر موضوع اضطراری است عدد 1 را ارسال کنید.")

    pending_emergency[event.sender_id] = {
        "original_text": text,
        "timestamp": datetime.now()
    }
