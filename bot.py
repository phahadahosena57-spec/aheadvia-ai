import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from google import genai

# -----------------------------
# Configuration
# -----------------------------

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -----------------------------
# Start Command
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AHEAD VIA AI-তে স্বাগতম!\n\n"
        "আমি আপনার AI assistant।\n"
        "আপনি আমাকে যেকোনো প্রশ্ন করতে পারেন।\n\n"
        "💬 আপনার প্রশ্ন লিখে পাঠান।"
    )

# -----------------------------
# AI Chat
# -----------------------------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=user_text,
        )

        answer = response.text

        if not answer:
            answer = "দুঃখিত, কোনো উত্তর পাওয়া যায়নি।"

        await update.message.reply_text(answer)

    except Exception as error:
        logging.error(error)

        await update.message.reply_text(
            "⚠️ AI-এর সাথে সংযোগ করতে সমস্যা হয়েছে। "
            "কিছুক্ষণ পরে আবার চেষ্টা করুন।"
        )

# -----------------------------
# Main
# -----------------------------

def main():

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    print("AHEAD VIA AI Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
