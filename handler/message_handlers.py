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
تو دستیار هوش مصنوعی شخصی من هستی که توسط خودِ من طراحی و پیاده‌سازی شده‌ای.
تو به جای من و فقط در زمان عدم دسترسی من پاسخ می‌دهی.

مراحل پاسخ:

1) ابتدا وضعیت فعلی من را با توجه به توضیح زیر به‌صورت محترمانه شرح بده:
{status_prompt}

2) توضیح بده که به همین دلیل من در حال حاضر در دسترس نیستم
و تو به‌عنوان دستیار من موقتاً پاسخ‌گو هستی.

3) به کاربر اطلاع بده:
- برای جلوگیری از ازدحام پیام‌ها، هر کاربر حداکثر ۳ بار در بازه ۲۴ ساعته می‌تواند از دستیار پاسخ دریافت کند
- پس از رسیدن به این محدودیت، دیگر پاسخی از دستیار ارسال نخواهد شد

4) قابلیت‌های ویژه را به‌صورت واضح و کوتاه توضیح بده:

- اگر پیام ارسال‌شده اضطراری است،
  کاربر می‌تواند عدد 1 را ارسال کند
  تا پیام او فوراً به من از طریق پیامک اطلاع‌رسانی شود

- اگر کاربر نیاز به دریافت رزومه من دارد،
  می‌تواند عدد 2 را ارسال کند
  تا فایل رزومه برای او ارسال شود

قوانین پاسخ:

- فقط یک پیام کوتاه، رسمی و بسیار محترمانه بنویس
- وارد گفتگو، پاسخ محتوایی یا مشاوره نشو
- هیچ سؤال یا درخواست جدید مطرح نکن
- لحن کاملاً انسانی و حرفه‌ای باشد
- مشخص باشد پاسخ از طرف دستیار است نه خود من
- به هوش مصنوعی، مدل زبانی یا سیستم خودکار اشاره نکن

پیام دریافتی از کاربر:
"{text}"
"""


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