"""test."""

# from simpleparser.mod1 import regex
# from simpleparser.prim import token
from simpleparser.mod1 import token, regex


def test_1() -> None:
    """test_1."""
    a: int = 1
    b: int = 1
    assert a == b


def test_token_1() -> None:
    """test_token_1."""
    f = token("foo")
    assert f.exec("foobar").tokens == ["foo"]


def test_regex_1() -> None:
    """test_regex_2."""
    f = regex("([1-9]+)")
    assert f.exec("123").tokens == ["123"]
