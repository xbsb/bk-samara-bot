import os
import telebot
from telebot import types
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

FIREBASE_URL = "https://bksamaralive-f48ec-default-rtdb.europe-west1.firebasedatabase.app/state.json"

# ---------- КНОПКИ ----------
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📍 Локация", "📏 Километры")
    kb.add("🔋 Батарея", "🗺 Карта")
    kb.add("ℹ️ Статус")
    return kb

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот управления запущен.\nВыбери действие:",
        reply_markup=main_keyboard()
    )

# ---------- ПОЛУЧЕНИЕ ДАННЫХ ----------
def get_state():
    r = requests.get(FIREBASE_URL, timeout=10)
    return r.json()

# ---------- КНОПКИ ----------
@bot.message_handler(func=lambda m: True)
def handler(message):
    data = get_state()

    if message.text == "📍 Локация":
        bot.send_message(
            message.chat.id,
            f"📍 Координаты:\n{data['lat']}, {data['lon']}"
        )

    elif message.text == "📏 Километры":
        bot.send_message(
            message.chat.id,
            f"📏 Пройдено: {data['distance']} км"
        )

    elif message.text == "🔋 Батарея":
        bot.send_message(
            message.chat.id,
            f"🔋 Батарея: {data['battery']}%"
        )

    elif message.text == "🗺 Карта":
        map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        bot.send_message(message.chat.id, f"🗺 Карта:\n{map_url}")

    elif message.text == "ℹ️ Статус":
        bot.send_message(
            message.chat.id,
            f"ℹ️ Статус:\n"
            f"📏 {data['distance']} км\n"
            f"🔋 {data['battery']}%\n"
            f"⏱ {data['ts']}"
        )

bot.infinity_polling()
