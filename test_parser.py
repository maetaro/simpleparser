"""test."""

from simple_parser import token


def test_1() -> None:
    """test_1."""
    a: int = 1
    b: int = 1
    assert a == b


def test_token_1() -> None:
    """test_token_1."""
    f = token("foo")
    assert f.exec("foobar").result() == ["foo"]
