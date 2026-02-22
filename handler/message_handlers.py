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

async def process_message(event, text, status_prompt, assistent):
    """ارسال پاسخ معمولی از دستیار و ثبت pending emergency"""

    final_prompt = f"""
        🟢 **تو دستیار هوش مصنوعی شخصی من هستی** که توسط خودم طراحی و پیاده‌سازی شده‌ای.

        ─────────────────────────────
        📌 **مراحل پاسخ:**

        1️⃣ **شرح وضعیت فعلی من:**  
        {status_prompt}

        2️⃣ **عدم دسترسی من:**  
        به همین دلیل من فعلاً در دسترس نیستم و تو به‌عنوان دستیار موقتاً پاسخ‌گو هستی.
        دقیقا همون چیزی که نوشته رو بازگو نکن بلکه بیا متن بهتر و زیباتر استفاده کن با ذهنیت خودت
        3️⃣ **قوانین تعامل با کاربر:**  
        - هر کاربر حداکثر **۳ پیام در ۲۴ ساعت** می‌تواند دریافت کند  
        - پس از رسیدن به این محدودیت، دیگر پاسخی از دستیار دریافت نخواهد شد
        - این رو برای کاربر بعضا یاداور باش

        4️⃣ **قابلیت‌های ویژه:**  
        - 🚨 **پیام اضطراری:** اگر پیام فوریت دارد، عدد `1` را ارسال کند تا پیام او فوراً از طریق **SMS** اطلاع‌رسانی شود  
        - 📄 **دریافت رزومه:** اگر نیاز به رزومه من دارد، عدد `2` را ارسال کند تا فایل PDF رزومه برای او ارسال شود
        - اگر به دنبال شرح حال هستن میتونی از لینک گیت هاب من استفاده کنی و سرچ بزنی و خودت شرحی بدی از من : https://github.com/amirhosein-kia-darbandsary

        ─────────────────────────────
        📝 **قوانین پاسخ:**

        - پاسخ باید کوتاه، رسمی، محترمانه و انسانی باشد  
        - مشخص باشد پاسخ از طرف دستیار است نه خود من  
        - از اشاره به هوش مصنوعی، مدل زبانی یا سیستم خودکار پرهیز کن

        ─────────────────────────────
        💬 **پیام دریافتی از کاربر:**  
        "{text}"

        ─────────────────────────────
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