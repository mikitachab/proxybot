import os

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
import redis
import emoji

import db


TOKEN = os.getenv("TOKEN")

redisc = redis.Redis()
proxy_db = db.ProxyBotDB(redisc)


def leave(update, context):
    chat_id = update.effective_chat.id
    proxy_db.remove_chat(chat_id)


def start(update, context):
    chat_id = update.effective_chat.id
    proxy_db.add_chat(chat_id)
    context.bot.send_message(chat_id=chat_id, text="Let's start")


def text_message(update, context):
    current_chat = proxy_db.get_chat_by_id(update.effective_chat.id)
    print(current_chat)
    chats_to_send = [chat for chat in proxy_db.get_chats() if chat.chat_id != current_chat.chat_id]
    message = emoji.emojize(f"{current_chat.emoji_alias}: {update.message.text}", use_aliases=True)
    print(message)
    print(type(message))
    for chat in chats_to_send:
        print(chat)
        context.bot.send_message(chat_id=chat.chat_id, text=message)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    text_filter = Filters.text & (~Filters.command)
    message_handler = MessageHandler(text_filter, text_message)
    start_handler = CommandHandler("start", start)
    leave_handler = CommandHandler("leave", leave)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(leave_handler)

    print("started polling")
    updater.start_polling()


if __name__ == "__main__":
    main()
