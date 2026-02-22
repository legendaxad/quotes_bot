import uuid

from loader import bot, db, quote_cache
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.quote_service import get_random_quote



@bot.message_handler(commands=["start"])
def start(message):
    db.add_user(message.chat.id)
    bot.send_message(message.chat.id,
                     "Welcome to Daily Quote bot \nType /quote to get inspiration.")


@bot.message_handler(commands=['quote'])
def quote(message):
    quote_text, author = get_random_quote()

    # generate unique short id
    quote_id = str(uuid.uuid4())[:8]

    # store in memory
    quote_cache[quote_id] = (quote_text, author)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "❤️ Save",
            callback_data=f"save:{quote_id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "📚 My Saved Quotes",
            callback_data="view_saved"
        )
    )

    bot.send_message(
        message.chat.id,
        f"{quote_text}\n\n— {author}\n\n- for more /quote",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data.startswith("save:"):
        quote_id = call.data.split(":")[1]

        if quote_id in quote_cache:
            quote_text, author = quote_cache[quote_id]

            db.save_quote(call.message.chat.id, quote_text, author)

            bot.answer_callback_query(call.id, "Saved ❤️")

            del quote_cache[quote_id]

    elif call.data == "view_saved":
        saved = db.get_saved_quotes(call.message.chat.id)

        if not saved:
            bot.send_message(call.message.chat.id, "No saved quotes yet.")
            return

        text = "📚 Your Saved Quotes:\n\n"
        for q in saved:
            text += f"{q['quote']}\n— {q['author']}\n\n"

        bot.send_message(call.message.chat.id, text)