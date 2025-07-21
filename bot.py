import os
import json
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7678239639:AAFdhhcJRVEFXx_P9wHoJ8Ox8_otKh9kAts")
ADMIN_ID = os.getenv("6844038711")

bot = telebot.TeleBot("7678239639:AAFdhhcJRVEFXx_P9wHoJ8Ox8_otKh9kAts")

def load_promos():
    with open("promos.json", "r") as f:
        return json.load(f)

def save_promos(promos):
    with open("promos.json", "w") as f:
        json.dump(promos, f, indent=2)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🎰 Добро пожаловать в ByteCasino бот!")

@bot.message_handler(commands=["promo"])
def create_promo(msg):
    if str(msg.from_user.id) != ADMIN_ID:
        return
    parts = msg.text.split()
    if len(parts) != 3:
        return bot.reply_to(msg, "Формат: /promo КОД СУММА")
    code, amount = parts[1], int(parts[2])
    promos = load_promos()
    promos[code] = {"amount": amount, "used_by": []}
    save_promos(promos)
    bot.reply_to(msg, f"Промо {code} создан на {amount} BCN")

@bot.message_handler(commands=["balance"])
def show_balance(msg):
    user_id = str(msg.from_user.id)
    with open("data.json", "r") as f:
        data = json.load(f)
    bal = data.get("users", {}).get(user_id, {}).get("balance", 0)
    bot.reply_to(msg, f"💰 Ваш баланс: {bal} BCN")

@bot.message_handler(commands=["setbalance"])
def set_balance(msg):
    if str(msg.from_user.id) != ADMIN_ID:
        return
    try:
        _, uid, amount = msg.text.split()
        uid = str(uid)
        amount = int(amount)
        with open("data.json", "r") as f:
            data = json.load(f)
        if uid not in data["users"]:
            data["users"][uid] = {"balance": 0}
        data["users"][uid]["balance"] = amount
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
        bot.reply_to(msg, f"Баланс {uid} установлен на {amount}")
    except:
        bot.reply_to(msg, "Формат: /setbalance ID СУММА")

bot.polling()
