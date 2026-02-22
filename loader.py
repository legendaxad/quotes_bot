
from telebot import TeleBot
import os
from database import Database

BOT_TOKEN = os.getenv("BOT_TOKEN")
#
TOKEN=""
bot=TeleBot(BOT_TOKEN)
db = Database()
db.create_tables()