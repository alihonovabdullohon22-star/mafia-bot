from flask import Flask
from threading import Thread
import telebot
import os
import random

# ===== KEEP ALIVE (24/7) =====
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== BOT =====
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ===== ADMIN =====
ADMIN_ID = 542998322
ADMIN_USERNAME = "@alihonov_a1"

# ===== DATA =====
games = {}
users = {}
referrals = {}

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

    # REFERAL
    if len(args) > 1:
        try:
            ref_id = int(args[1])
            if user_id != ref_id:
                referrals[user_id] = ref_id
                get_user(ref_id)["coin"] += 20
                bot.send_message(ref_id, "🎁 Referal +20 coin!")
        except:
            pass

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 Join", "🚀 Start")
    markup.add("💰 Balance", "🛒 Shop")
    markup.add("💳 Buy Coin", "👥 Referal")

    bot.send_message(msg.chat.id,
    "🎭 <b>MAFIA BOT</b>\n\n"
    "🔥 Eng zo‘r o‘yin bot!\n\n"
    "💰 Coin yig‘ib pul ishlang!\n\n"
    f"👤 Admin: {ADMIN_USERNAME}",
    parse_mode="HTML",
    reply_markup=markup)

# ===== JOIN =====
@bot.message_handler(func=lambda m: m.text == "🎮 Join")
def join(msg):
    game = get_game(msg.chat.id)
    user_id = msg.from_user.id
    name = msg.from_user.first_name

    if user_id not in game["players"]:
        game["players"].append(user_id)
        bot.send_message(msg.chat.id,
        f"🎮 <b>{name}</b> qo‘shildi!\n👥 {len(game['players'])} ta",
        parse_mode="HTML")
    else:
        bot.send_message(msg.chat.id, "❗ Siz allaqachon qo‘shilgansiz")

# ===== START GAME =====
@bot.message_handler(func=lambda m: m.text == "🚀 Start")
def start_game(msg):
    game = get_game(msg.chat.id)

    if len(game["players"]) < 3:
        bot.send_message(msg.chat.id, "❗ Kamida 3 ta o‘yinchi kerak")
        return

    players = game["players"]
    winner = random.choice(players)

    get_user(winner)["coin"] += 30

    user_info = bot.get_chat(winner)
    name = user_info.first_name

    bot.send_message(msg.chat.id,
    f"🏆 <b>G‘OLIB:</b> {name}\n💰 +30 coin",
    parse_mode="HTML")

    games[msg.chat.id] = {"players": [], "started": False}

# ===== BALANCE =====
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(msg):
    bot.send_message(msg.chat.id,
    f"💰 <b>Balans:</b>\n🪙 {get_user(msg.from_user.id)['coin']} coin",
    parse_mode="HTML")

# ===== SHOP =====
@bot.message_handler(func=lambda m: m.text == "🛒 Shop")
def shop(msg):
    bot.send_message(msg.chat.id,
    "🛒 Shop:\nVIP = 100 coin")

# ===== REFERAL =====
@bot.message_handler(func=lambda m: m.text == "👥 Referal")
def referal(msg):
    link = f"https://t.me/{bot.get_me().username}?start={msg.from_user.id}"
    bot.send_message(msg.chat.id,
    f"👥 Referal link:\n\n{link}\n\n+20 coin")

# ===== BUY COIN =====
@bot.message_handler(func=lambda m: m.text == "💳 Buy Coin")
def buy(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Check Payment")

    bot.send_message(msg.chat.id,
    "💳 CLICK to‘lov:\n\n"
    "100 coin = 10 000 so‘m\n\n"
    "📱 9860160129222933\n\n"
    f"👤 Admin: {ADMIN_USERNAME}",
    reply_markup=markup)

# ===== CHECK PAYMENT =====
@bot.message_handler(func=lambda m: m.text == "✅ Check Payment")
def check(msg):
    get_user(msg.from_user.id)["coin"] += 100
    bot.send_message(msg.chat.id,
    "✅ To‘lov tasdiqlandi!\n💰 +100 coin")

# ===== ADMIN =====
@bot.message_handler(commands=['give'])
def give(msg):
    if msg.from_user.id != ADMIN_ID:
        return

    try:
        _, uid, amount = msg.text.split()
        uid = int(uid)
        amount = int(amount)

        get_user(uid)["coin"] += amount
        bot.send_message(uid, f"💰 +{amount} coin")
    except:
        bot.send_message(msg.chat.id, "❗ xato")

# ===== RUN =====
keep_alive()
bot.infinity_polling()
