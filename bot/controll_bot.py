import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import httpx
from dotenv import load_dotenv

# ================= CONFIG =================
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FASTAPI_BASE = "http://localhost:9999"  # فرض بر FastAPI است

# وضعیت‌ها
WORK_STATUS_PROMPTS = {
    "coding": (
        "در حال کدنویسی عمیق هستم و تمرکز کامل دارم. "
        "فعلاً امکان پاسخ‌گویی ندارم. "
        "اگر موضوع خیلی ضروری است، لطفاً فقط یک پیام کوتاه بفرستید "
        "یا در صورت فوریت از طریق پیامک اطلاع دهید."
    ),
    "deep-work": (
        "در حال انجام کار عمیق و بدون وقفه هستم. "
        "برای حفظ تمرکز فعلاً پاسخ نمی‌دهم. "
        "در اولین فرصت پیام شما را بررسی می‌کنم."
    ),
    "on-way": (
        "در حال حرکت و خارج از دسترس هستم و فعلاً امکان بررسی تلگرام را ندارم. "
        "به محض رسیدن پاسخ می‌دهم. "
        "اگر موضوع ضروری است، لطفاً پیامک ارسال کنید."
    ),
    "meeting": (
        "در حال جلسه هستم و امکان پاسخ‌گویی ندارم. "
        "بعد از پایان جلسه پیام شما را بررسی می‌کنم."
    ),
    "sleeping": (
        "در حال استراحت هستم و فعلاً در دسترس نیستم. "
        "پس از بیدار شدن پاسخ می‌دهم."
    ),
    "no-connection": (
        "در حال حاضر به اینترنت دسترسی ندارم و امکان اتصال به تلگرام وجود ندارد. "
        "پس از برقراری اتصال پاسخ‌گو خواهم بود."
    ),
    "busy": (
        "در حال رسیدگی به چند کار هم‌زمان هستم و ممکن است پاسخ با تأخیر انجام شود. "
        "پیام شما ثبت شد و در اولین فرصت پاسخ می‌دهم."
    ),
    "urgent-only": (
        "فعلاً فقط پیام‌های فوری را بررسی می‌کنم. "
        "اگر موضوع شما ضروری است، لطفاً به‌صورت خلاصه اطلاع دهید."
    ),
    "offline": (
        "در حال حاضر آفلاین هستم و پیام‌ها را بعداً بررسی می‌کنم."
    ),
    "free":("کاربر انلاین است در اسرع وقت انلاین خواهد شد")
}

# ================= HELPERS =================
async def set_status_on_server(status_key: str):
    """ارسال وضعیت به FastAPI"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{FASTAPI_BASE}/status", json={"status": status_key})
        resp.raise_for_status()
        return resp.json()


# ================= HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دکمه شیشه‌ای برای همه وضعیت‌ها
    keyboard = []
    row = []
    for i, key in enumerate(WORK_STATUS_PROMPTS.keys(), start=1):
        row.append(InlineKeyboardButton(key, callback_data=f"set_status:{key}"))
        if i % 2 == 0:  # دو دکمه در هر ردیف
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("وضعیت کاری خود را انتخاب کنید:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("set_status:"):
        status_key = query.data.split(":")[1]
        try:
            # آپدیت وضعیت روی سرور
            await set_status_on_server(status_key)
            # پاسخ به کاربر با متن وضعیت
            text = WORK_STATUS_PROMPTS.get(status_key, "وضعیت نامشخص")
            await query.edit_message_text(f"وضعیت شما بروزرسانی شد:\n\n{text}")
        except Exception as e:
            await query.edit_message_text(f"خطا در بروزرسانی وضعیت:\n{e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start — انتخاب وضعیت کاری")

# ================= MAIN =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()