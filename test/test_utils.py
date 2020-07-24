import bytes_utils


def test_bytes_to_str():
    bytes_ = bytes(b"abc")
    assert bytes_utils.bytes_to_str(bytes_) == "abc"
