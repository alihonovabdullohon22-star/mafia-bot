import telebot
import os

TOKEN = os.getenv("8749094325:AAFBmaqer-Y_rDiSsKTzytzwyG5HNrRlp70")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🎭 Mafia bot ishlayapti!")

bot.polling()
