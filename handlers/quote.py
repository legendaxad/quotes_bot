from loader import bot,db
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.quote_service import get_random_quote



@bot.message_handler(commands=["start"])
def start(message):
    db.add_user(message.chat.id)
    bot.send_message(message.chat.id,
                     "Welcome to Daily Quote bot \nType /quote to get inspiration.")


@bot.message_handler(commands=['quote'])
def quote(message):
    quote_text,author=get_random_quote()
    markup=InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "❤️ Save",
            callback_data=f"save | {quote_text}|{author}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "My saved quotes",
            callback_data="view_saved"
        )
    )

    bot.send_message(message.chat.id,
                     f"{quote_text}\n\n- {author}",reply_markup=markup),

@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    if call.data.startwith("save|"):
        _,quote,author=call.data.split("|",2)
        db.save_quote(call.message.chat.id,quote,author)
        bot.answer_callback_query(call.id,"Saved")

    elif call.data=="view_saved":
        saved_quotes=db.get_saved_quotes(call.message.chat.id)
        if not saved_quotes:
            bot.send_message(
                call.message.chat.id,
                "You do not have saved quotes yet."
            )
            return
        text="Your Saved Quotes:\n\n"

        for q in saved_quotes:
            text+=f"{q['quote']}\n- {q['author']}\n\n"

        bot.send_message(call.message.chat.id,text)