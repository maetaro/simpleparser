"""a parser function's combinator."""

from typing import List, Callable
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def many(parser: Parser) -> Parser:
    """Many function.

    Parameters
    ----------
    parser
        The Parser object.

    Returns
    -------
    Parser
        generated new Paraser object.

    Example
    -------
    >>> from simpleparser import many, token
    >>> p = many(token("foo"))
    >>> p.exec('')
    []
    >>> p.exec('foo')
    ['foo']
    >>> p.exec('foofoo')
    ['foo', 'foo']
    >>> p.exec('bar')
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            result.extend(parsed.tokens)
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def choice(*args: Parser) -> Parser:
    """Choice function.

    Parameters
    ----------
    *args
        The Parser objects.

    Returns
    -------
    Parser
        generated new Paraser object.

    Example
    -------
    >>> from simpleparser import token, choice
    >>> p = choice(token('foo'), token('bar'))
    >>> p.exec('foo')
    ['foo']
    >>> p.exec('bar')
    ['bar']
    >>> p.exec('alice')
    parse error at (0): unexpected ali expecting foo
    parse error at (0): unexpected ali expecting bar
    """
    parsers = args

    def f(target: str, position: int = 0) -> ParseResult:
        messages = []
        for parser in parsers:
            parsed = parser.exec(target, position)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position)

    return Parser(f)


def seq(*args: Parser) -> Parser:
    r"""Seq function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> parse = seq(token('foo'), choice(token('bar'), token('baz')))
    >>> parse.exec('foobar')
    ['foo', 'bar']
    >>> parse.exec('foobaz')
    ['foo', 'baz']
    >>> parse.exec('foo')
    parse error at (3): unexpected  expecting bar
    parse error at (3): unexpected  expecting baz
    """  # noqa: E501
    parsers = args

    def f(target: str, position: int = 0) -> ParseResult:
        result: List[str] = []
        pos_org = position
        for parser in parsers:
            parsed: ParseResult = parser.exec(target, position)
            if not parsed.success:
                return Failure(parsed.message, pos_org)
            if parsed.tokens is None:
                continue
            result.extend(parsed.tokens)
            position = parsed.position

        return Success(result, position)

    return Parser(f)


def option(parser: Parser) -> Parser:
    """Option function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> parser = option(token('hoge'))
    >>> parser.exec('hoge', 0)
    ['hoge']
    >>> parser.exec('fuga', 0)
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if result.success:
            return result
        return Success([], position)

    return Parser(f)


def transform(parser: Parser, selector: Callable[[List[str]], List[str]]) -> Parser:
    """Map function.

    Example
    -------
    >>> from simpleparser import token, transform
    >>> transform(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo")
    ['foo aaa']
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if not result.success:
            return result
        result.tokens = selector(result.tokens)
        return result

    return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
