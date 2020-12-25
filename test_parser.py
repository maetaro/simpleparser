"""test."""

from simple_parser.simple_parser import char, token, Success

def test_1() -> None:
    """test_1."""
    a: int = 1
    b: int = 1
    assert a == b


def test_token_1() -> None:
    f = char("foo")
    assert f.exec("foobar").result() == ["foo"]
