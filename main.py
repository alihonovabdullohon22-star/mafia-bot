77701"}
import telebot
import os
import random

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 542998322
ADMIN_USERNAME = "@alihonov_a1"

games = {}
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"coin": 0}
    return users[user_id]

def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = {
            "players": [],
            "roles": {},
            "started": False,
            "votes": {}
        }
    return games[chat_id]

# ===== START =====
@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 Join", "🚀 Start")

    bot.send_message(msg.chat.id,
    "🎭 Mafia game boshlash uchun Join bosing",
    reply_markup=markup)

# ===== JOIN =====
@bot.message_handler(func=lambda m: m.text == "🎮 Join")
def join(msg):
    game = get_game(msg.chat.id)
    uid = msg.from_user.id

    if uid not in game["players"]:
        game["players"].append(uid)
        bot.send_message(msg.chat.id,
        f"👤 Qo‘shildi ({len(game['players'])})")

# ===== START GAME =====
@bot.message_handler(func=lambda m: m.text == "🚀 Start")
def start_game(msg):
    game = get_game(msg.chat.id)

    if len(game["players"]) < 3:
        bot.send_message(msg.chat.id, "Kamida 3 kishi kerak")
        return

    game["started"] = True

    players = game["players"]
    random.shuffle(players)

    roles = {}
    roles[players[0]] = "😈 Mafia"
    roles[players[1]] = "👮 Sheriff"

    for p in players[2:]:
        roles[p] = "👤 Oddiy"

    game["roles"] = roles

    # private role
    for uid, role in roles.items():
        try:
            bot.send_message(uid, f"Siz: {role}")
        except:
            pass

    bot.send_message(msg.chat.id,
    "🌙 Kecha boshlandi...")

    # mafia kill (random)
    mafia = players[0]
    victim = random.choice(players[1:])

    game["dead"] = victim

    bot.send_message(msg.chat.id,
    "☀️ Kun boshlandi!\n/vote id yozing")

# ===== VOTE =====
@bot.message_handler(commands=['vote'])
def vote(msg):
    game = get_game(msg.chat.id)

    try:
        target = int(msg.text.split()[1])
    except:
        bot.send_message(msg.chat.id, "❗ /vote id")
        return

    game["votes"].setdefault(target, 0)
    game["votes"][target] += 1

    if game["votes"][target] >= 2:
        finish(msg.chat.id)

# ===== FINISH =====
def finish(chat_id):
    game = get_game(chat_id)

    winner = random.choice(game["players"])
    get_user(winner)["coin"] += 30

    name = bot.get_chat(winner).first_name

    bot.send_message(chat_id,
    f"🏆 G‘olib: {name}\n💰 +30 coin")

    games[chat_id] = {
        "players": [],
        "roles": {},
        "started": False,
        "votes": {}
    }

bot.infinity_polling()
