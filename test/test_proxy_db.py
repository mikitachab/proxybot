import pytest
import db


@pytest.fixture
def redis_stub(mocker):
    return mocker.stub(name="redis_stub")


@pytest.fixture
def proxy_db(redis_stub):
    prdb = db.ProxyBotDB(redis_stub)
    return prdb


def test_proxy_db_make_chat_key(proxy_db):
    key = proxy_db.make_chat_key("123")
    assert key == "proxybotchat;123"


def test_proxy_db_make_emoji_key(proxy_db):
    key = proxy_db.make_emoji_key(":emoji:")
    assert key == "proxybotemoji;:emoji:"


def test_proxy_db_get_value_from_key(proxy_db):
    key = "proxybotchat;123"
    assert proxy_db.get_value_from_key(key) == "123"
