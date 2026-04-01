from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
import telebot
import os
import random

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ===== ADMIN =====
ADMIN_ID = 542998322  # <-- o‘zingni ID qo‘y

# ===== DATA =====
games = {}
users = {}

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"coin": 0}
    return users[user_id]

# ===== GAME =====
def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = {
            "players": [],
            "started": False
        }
    return games[chat_id]

# ===== START =====
@bot.message_handler(commands=['start'])
def start(msg):
    args = msg.text.split()

    user_id = msg.from_user.id

    # referal ishlashi
    if len(args) > 1:
        ref_id = int(args[1])
        if user_id != ref_id:
            referrals[user_id] = ref_id

            ref_user = get_user(ref_id)
            ref_user["coin"] += 10

            bot.send_message(ref_id, "🎁 Siz referal uchun +10 coin oldingiz!")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 Join", "🚀 Start")
    markup.add("💰 Balance", "🛒 Shop")
    markup.add("💳 Buy Coin", "👥 Referal")

    bot.send_message(msg.chat.id,
    "🎭 Mafia bot\n👇 Tugmalardan foydalaning",
    reply_markup=markup)

# ===== JOIN =====
@bot.message_handler(func=lambda m: m.text == "🎮 Join")
def join(msg):
    game = get_game(msg.chat.id)
    user_id = msg.from_user.id
    name = msg.from_user.first_name

    if user_id not in game["players"]:
        game["players"].append(user_id)

        bot.send_message(
            msg.chat.id,
            f"✅ {name} qo‘shildi ({len(game['players'])} ta)"
        )
    else:
        bot.send_message(msg.chat.id, "❗ Siz allaqachon qo‘shilgansiz")

# ===== START GAME =====
@bot.message_handler(func=lambda m: m.text == "🚀 Start")
def start_game(msg):
    game = get_game(msg.chat.id)

    if game["started"]:
        bot.send_message(msg.chat.id, "⚠️ O‘yin allaqachon boshlangan")
        return

    if len(game["players"]) < 3:
        bot.send_message(msg.chat.id, "❗ Kamida 3 ta o‘yinchi kerak")
        return

    game["started"] = True

    players = game["players"]
    winner = random.choice(players)

    # 💰 faqat g‘olibga coin
    user = get_user(winner)
    user["coin"] += 30

    user_info = bot.get_chat(winner)
    name = user_info.username if user_info.username else user_info.first_name

    bot.send_message(
        msg.chat.id,
        f"🏆 G‘olib: {name}\n💰 +30 coin berildi!"
    )

    # RESET
    games[msg.chat.id] = {
        "players": [],
        "started": False
    }

# ===== BALANCE =====
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(msg):
    user = get_user(msg.from_user.id)
    bot.send_message(msg.chat.id, f"💰 Sizning coin: {user['coin']}")

# ===== SHOP =====
@bot.message_handler(func=lambda m: m.text == "🛒 Shop")
def shop(msg):
    bot.send_message(
        msg.chat.id,
        "🛒 Shop:\n\n"
        "VIP — 100 coin\n"
        "Lucky — 50 coin"
    )

# ===== BUY COIN (CLICK) =====
@bot.message_handler(func=lambda m: m.text == "💳 Buy Coin")
def buy_coin(msg):
    bot.send_message(
        msg.chat.id,
        "💳 CLICK orqali to‘lov:\n\n"
        "💰 100 coin = 10 000 so‘m\n\n"
        "📱https://t.me/alihonov_a1\n\n"
        "To‘lovdan keyin admin ga yozing"
    )

# ===== ADMIN GIVE =====
@bot.message_handler(commands=['give'])
def give_coin(msg):
    if msg.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id, amount = msg.text.split()
        user_id = int(user_id)
        amount = int(amount)

        user = get_user(user_id)
        user["coin"] += amount

        bot.send_message(msg.chat.id, "✅ Coin berildi")
        bot.send_message(user_id, f"💰 Sizga {amount} coin berildi!")

    except:
        bot.send_message(msg.chat.id, "❗ Format: /give user_id coin")

keep_alive()
# ===== RUN =====
bot.infinity_polling()
