import collections

import emoji_utils
import bytes_utils


Chat = collections.namedtuple("Chat", "chat_id, emoji_alias")


class ProxyBotDB:
    def __init__(self, redis):
        self.redis = redis
        self.db_prefix = "proxybot"
        self.chat_prefix = "chat"
        self.emoji_prefix = "emoji"
        self.prefix_sep = ";"

    def make_chat_key(self, chat_id):
        return f"{self.db_prefix}{self.chat_prefix}{self.prefix_sep}{chat_id}"

    def make_emoji_key(self, emoji_alias):
        return f"{self.db_prefix}{self.emoji_prefix}{self.prefix_sep}{emoji_alias}"

    def get_value_from_key(self, key):
        return key.split(self.prefix_sep)[1]

    def add_chat(self, chat_id):
        chat_key = self.make_chat_key(chat_id)
        emoji_alias = self.get_unique_emoji_alias()
        emoji_alias_key = self.make_emoji_key(emoji_alias)
        self.redis.set(chat_key, emoji_alias)
        self.redis.set(emoji_alias_key, chat_id)

    def get_chats(self):
        chat_prefix = self.db_prefix + self.chat_prefix
        chats_keys = [bytes_utils.bytes_to_str(k) for k in self.redis.keys(f"{chat_prefix}*")]
        chats = []
        for chat_key in chats_keys:
            chat_id = int(self.get_value_from_key(chat_key))
            emoji_alias = self.redis.get(chat_key)
            chats.append(Chat(chat_id, emoji_alias))
        return chats

    def remove_chat(self, chat_id):
        key = self.make_chat_key(chat_id)
        emoji_alias = bytes_utils.bytes_to_str(self.redis.get(key))
        emoji_alias_key = self.make_emoji_key(emoji_alias)
        self.redis.delete(key, emoji_alias_key)

    def get_unique_emoji_alias(self):
        while True:
            emoji_alias = emoji_utils.get_random_emoji_alias()
            emoji_key = self.make_emoji_key(emoji_alias)
            if not self.redis.get(emoji_key):
                return emoji_alias

    def get_chat_by_id(self, chat_id):
        chat_key = self.make_chat_key(chat_id)
        emoji_alias = bytes_utils.bytes_to_str(self.redis.get(chat_key))
        if emoji_alias:
            return Chat(int(chat_id), emoji_alias)
        return None
