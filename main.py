import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

players = []
game_active = False

# 🎮 Menu
def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎮 Join"), KeyboardButton("🚀 Start"))
    return markup

# 🔹 Start
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🎭 Mafia botga xush kelibsiz!", reply_markup=menu())

# 🔹 Join (button)
def join(msg):
    if msg.from_user.id not in players:
        players.append(msg.from_user.id)
        bot.send_message(msg.chat.id, "✅ Siz o‘yinga qo‘shildingiz")
    else:
        bot.send_message(msg.chat.id, "⚠️ Siz allaqachon qo‘shilgansiz")

# 🔹 Start game
def start_game(msg):
    global game_active
    
    if len(players) < 3:
        bot.send_message(msg.chat.id, "❌ Kamida 3 ta odam kerak")
        return
    
    game_active = True
    
    mafia = random.choice(players)
    doctor = random.choice(players)

    for p in players:
        if p == mafia:
            bot.send_message(p, "🔪 Siz MAFIYAsiz")
        elif p == doctor:
            bot.send_message(p, "💉 Siz DOCTORSIZ")
        else:
            bot.send_message(p, "👨‍🌾 Siz oddiy odamsiz")

    bot.send_message(msg.chat.id, "🎮 O‘yin boshlandi!")

# 🔹 COMMANDS ham ishlasin
@bot.message_handler(commands=['join'])
def join_cmd(msg):
    join(msg)

@bot.message_handler(commands=['startgame'])
def start_cmd(msg):
    start_game(msg)

# 🔹 BUTTON text ishlashi uchun
@bot.message_handler(content_types=['text'])
def all_messages(msg):
    if msg.text == "🎮 Join":
        join(msg)
    elif msg.text == "🚀 Start":
        start_game(msg)

# 🚀 RUN
bot.infinity_polling()
