import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
FIREBASE_URL = "https://bksamaralive-f48ec-default-rtdb.europe-west1.firebasedatabase.app/state.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 BK Samara bot запущен\n\n"
        "Команды:\n"
        "/status — текущие данные\n"
        "/link — ссылка на карту"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(FIREBASE_URL, timeout=5)
        data = r.json()

        text = (
            f"📍 Координаты:\n"
            f"Lat: {data.get('lat')}\n"
            f"Lon: {data.get('lon')}\n\n"
            f"🚶‍♂️ Пройдено: {data.get('distance')} м\n"
            f"🔋 Батарея: {data.get('battery')}%\n"
            f"🕒 Обновлено: {data.get('ts')}"
        )
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text("❌ Ошибка получения данных")

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗺 Карта:\n"
        "https://bksamaralive-f48ec-default-rtdb.europe-west1.firebasedatabase.app/state.json"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("link", link))

    app.run_polling()

if __name__ == "__main__":
    main()
