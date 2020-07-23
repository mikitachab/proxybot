import os
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import redis
import emoji

TOKEN = os.getenv("TOKEN")
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
redisc = redis.Redis()


class ChatList:
    def __init__(self, list_name):
        self.redis = redis.Redis()
        self.list_name = list_name

    def add_chat(self, chat_id):
        self.redis.rpush(self.list_name, chat_id)

    def get_chats(self):
        return [int(chat) for chat in self.redis.lrange(self.list_name, 0, -1)]


chat_list = ChatList("chatlist")


def get_random_emoji_alias():
    return random.choice(list(emoji.EMOJI_ALIAS_UNICODE.keys()))


def start(update, context):
    chat_id = update.effective_chat.id
    chat_list.add_chat(chat_id)
    redisc.set(chat_id, get_random_emoji_alias())
    context.bot.send_message(chat_id=chat_id, text="Let's start")


def text_message(update, context):
    current_chat = update.effective_chat.id
    chats_to_send = [chat for chat in chat_list.get_chats() if chat != current_chat]
    prefix = redisc.get(current_chat)
    message = emoji.emojize(f"{prefix}: {update.message.text}", use_aliases=True)
    for chat in chats_to_send:
        context.bot.send_message(chat_id=chat, text=message)


text_filter = Filters.text & (~Filters.command)
message_handler = MessageHandler(text_filter, text_message)
start_handler = CommandHandler("start", start)


def main():
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    print("started polling")
    updater.start_polling()


if __name__ == "__main__":
    main()
