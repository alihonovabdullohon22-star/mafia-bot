import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ===== ADMIN =====
ADMIN_ID = 542998322  # o‘zingni ID qo‘y

# ===== DATA =====
games = {}
users = {}

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"coin": 100}
    return users[user_id]

# ===== GAME =====
def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = {"players": {}, "started": False}
    return games[chat_id]

# ===== START =====
@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 Join", "🚀 Start")
    markup.add("🛒 Shop", "💰 Balance")
    markup.add("💳 Buy Coin")

    bot.send_message(
        msg.chat.id,
        "🎭 Mafia botga xush kelibsiz!\n\n👇 Tugmalardan foydalaning",
        reply_markup=markup
    )

# ===== JOIN =====
def join(msg):
    game = get_game(msg.chat.id)
    user_id = msg.from_user.id
    name = msg.from_user.first_name

    if game["started"]:
        bot.send_message(msg.chat.id, "⚠️ O‘yin boshlangan")
        return

    if user_id not in game["players"]:
        game["players"][user_id] = name

        user = get_user(user_id)
        user["coin"] += 10

        bot.send_message(
            msg.chat.id,
            f"✅ {name} qo‘shildi ({len(game['players'])} ta)\n💰 +10 coin"
        )
    else:
        bot.send_message(msg.chat.id, "❗ Siz allaqachon qo‘shilgansiz")

# ===== START GAME =====
def start_game(msg):
    game = get_game(msg.chat.id)

    if game["started"]:
        bot.send_message(msg.chat.id, "⚠️ O‘yin boshlangan")
        return

    if len(game["players"]) < 3:
        bot.send_message(msg.chat.id, "❗ Kamida 3 ta o‘yinchi kerak")
        return

    game["started"] = True
    players = list(game["players"].values())

    bot.send_message(
        msg.chat.id,
        "🚀 O‘yin boshlandi!\n\n👥 O‘yinchilar:\n" + "\n".join(players)
    )

# ===== SHOP =====
def shop(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💎 VIP (100)", "🎭 Skin (50)")
    markup.add("⬅️ Back")

    bot.send_message(msg.chat.id, "🛒 SHOP:", reply_markup=markup)

# ===== BUY ITEM =====
def buy(msg):
    user = get_user(msg.from_user.id)

    if msg.text == "💎 VIP (100)":
        if user["coin"] >= 100:
            user["coin"] -= 100
            bot.send_message(msg.chat.id, "✅ VIP oldingiz")
        else:
            bot.send_message(msg.chat.id, "❗ Coin yetarli emas")

    elif msg.text == "🎭 Skin (50)":
        if user["coin"] >= 50:
            user["coin"] -= 50
            bot.send_message(msg.chat.id, "✅ Skin oldingiz")
        else:
            bot.send_message(msg.chat.id, "❗ Coin yetarli emas")

# ===== BALANCE =====
@bot.message_handler(commands=['balance'])
def balance(msg):
    user = get_user(msg.from_user.id)
    bot.send_message(msg.chat.id, f"💰 Balans: {user['coin']} coin")

# ===== BUY COIN (CLICK) =====
def buy_coin(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Check Payment", "⬅️ Back")

    bot.send_message(
        msg.chat.id,
        "💳 CLICK orqali to‘lov:\n\n"
        "💰 100 coin = 10 000 so‘m\n\n"
        "📲 CLICK: 9860160129222933\n\n"
        "To‘lov qilgach 'Check Payment' bosing",
        reply_markup=markup
    )

# ===== CHECK PAYMENT =====
def check_payment(msg):
    user = get_user(msg.from_user.id)

    # Fake auto system (demo)
    user["coin"] += 100

    bot.send_message(
        msg.chat.id,
        "✅ To‘lov tasdiqlandi!\n💰 +100 coin qo‘shildi"
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

# ===== RESET =====
@bot.message_handler(commands=['reset'])
def reset(msg):
    games[msg.chat.id] = {"players": {}, "started": False}
    bot.send_message(msg.chat.id, "♻️ O‘yin reset qilindi")

# ===== HANDLER =====
@bot.message_handler(func=lambda msg: True)
def all_messages(msg):
    text = msg.text.lower()

    if text in ["🎮 join", "/join"]:
        join(msg)

    elif text in ["🚀 start", "/game"]:
        start_game(msg)

    elif text in ["🛒 shop", "/shop"]:
        shop(msg)

    elif text in ["💰 balance"]:
        balance(msg)

    elif text in ["💳 buy coin"]:
        buy_coin(msg)

    elif text == "✅ check payment":
        check_payment(msg)

    elif "vip" in text or "skin" in text:
        buy(msg)

    elif text == "⬅️ back":
        start(msg)

# ===== RUN =====
bot.infinity_polling()
