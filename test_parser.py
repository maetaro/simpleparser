"""test."""

from simpleparser import token, regex


def test_1() -> None:
    """test_1."""
    a: int = 1
    b: int = 1
    assert a == b


def test_token_1() -> None:
    """test_token_1."""
    f = token("foo")
    assert f.exec("foobar").tokens == ["foo"]


def test_token_2() -> None:
    """test_token_2."""
    f = token("foo")

    def success(result):
        assert True, "It was executed even though the parse failed."

    def fail(result):
        assert result.success is False
        assert result.message == "parse error at (0): unexpected fii expecting foo"  # noqa F501

    f.exec("fiibar").then(success).catch(fail)


def test_regex_1() -> None:
    """test_regex_2."""
    f = regex("([1-9]+)")
    assert f.exec("123").tokens == ["123"]
