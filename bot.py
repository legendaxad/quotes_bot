

from loader import bot
import handlers


if __name__=="__main__":
    print("Bot is running")
    bot.infinity_polling(skip_pending=True)
