import random
import emoji


def get_random_emoji_alias():
    return random.choice(list(emoji.EMOJI_ALIAS_UNICODE.keys()))
