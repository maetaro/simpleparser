"""test of ParseResult."""

from simpleparser import token, Parser, ParseResult


def test_then_1() -> None:
    """test_then_1."""
    f: Parser = token("foo")

    def f_then(result: ParseResult) -> None:
        assert result.tokens == ["foo"]

    def f_catch(result: ParseResult) -> None:
        assert False, "成功した場合は空振りする必要がある。"

    assert f.exec("foobar").then(f_then).catch(f_catch)


def test_catch_1() -> None:
    """test_catch_1."""
    f: Parser = token("bar")

    def f_then(result: ParseResult) -> None:
        assert False, "失敗した場合は空振りする必要がある。"

    def f_catch(result: ParseResult) -> None:
        assert result.tokens == []

    assert f.exec("foobar").then(f_then).catch(f_catch)
