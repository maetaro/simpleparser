"""test."""

from simpleparser import token, regex, Parser, ParseResult


def test_1() -> None:
    """test_1."""
    a: int = 1
    b: int = 1
    assert a == b


def test_token_1() -> None:
    """test_token_1."""
    f: Parser = token("foo")
    assert f.exec("foobar").tokens == ["foo"]


def test_token_2() -> None:
    """test_token_2."""
    f = token("foo")

    def success(result: ParseResult) -> None:
        assert True, "It was executed even though the parse failed."

    def fail(result: ParseResult) -> None:
        assert result.success is False
        assert result.message == "parse error at (0): unexpected fii expecting foo (by token)"  # noqa F501

    f.exec("fiibar").then(success).catch(fail)


def test_regex_1() -> None:
    """test_regex_2."""
    f = regex("([1-9]+)")
    assert f.exec("123").tokens == ["123"]


def test_none_of_1() -> None:
    from simpleparser import none_of, choice, token, many, transform
    quotedChar = choice(token('""'), none_of('"'))
    p = transform(many(quotedChar), lambda x: ["".join(x)])
    text = r'Shirt with ""Haskell"" text"'
    assert p.exec(text).tokens == ['Shirt with ""Haskell"" text']
