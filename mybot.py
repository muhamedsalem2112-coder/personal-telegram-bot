import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# قراءة البيانات من Environment Variables (من Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")
YOUR_TELEGRAM_ID = int(os.getenv("YOUR_TELEGRAM_ID"))

memory = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_TELEGRAM_ID:
        return
    await update.message.reply_text("🤖 بوتك الشخصي يعمل بنجاح!")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global memory
    if update.effective_user.id != YOUR_TELEGRAM_ID:
        return
    memory = []
    await update.message.reply_text("🗑️ تم مسح الذاكرة.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global memory
    
    if update.effective_user.id != YOUR_TELEGRAM_ID:
        return

    user_text = update.message.text
    memory.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": memory
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        await update.message.reply_text("❌ حدث خطأ في الاتصال بـ OpenAI")
        return

    reply = response.json()["choices"][0]["message"]["content"]
    memory.append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

app = ApplicationBuilder