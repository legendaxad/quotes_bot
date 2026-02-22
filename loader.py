
from telebot import TeleBot
import os
from database import Database

BOT_TOKEN = os.getenv("BOT_TOKEN")
# 7578223868:AAGxOjOe7E5VqoePyiqx2LOc9_mOlXrtYss
TOKEN=""
bot=TeleBot(BOT_TOKEN)
db = Database()
db.create_tables()