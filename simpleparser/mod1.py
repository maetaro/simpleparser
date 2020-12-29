"""a simple parser combinator."""

from typing import Callable, List
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def noneOf(s: str) -> Parser:
    """
    As the dual of oneOf, noneOf cs succeeds if the current character not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
    >>> from simpleparser import noneOf
    >>> noneOf("abcdefg").exec("hello", 0)
    ['h']
    """  # noqa: E501
    def f(target: str, position: int = 0) -> ParseResult:
        exists: bool = False
        targetChar: str = target[position:position + 1]
        for c in s:
            if targetChar == c:
                exists = True
                break
        if not exists:
            return Success([targetChar], position + 1)
        return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)  # noqa: E501

    return Parser(f)


def endBy(parser: Parser, sep: Parser) -> Parser:
    r"""Endby p sep parses zero or more occurrences of p, separated and ended by sep.

    Returns a list of values returned by p.

    Example
    -------
    >>> from simpleparser import token, regex, endBy
    >>> endBy(regex('\w*'), token(',')).exec('')
    ['']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge')
    ['hoge', 'hoge']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge,')
    ['hoge', 'hoge', '']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge,-')
    parse error.
    """  # noqa: D401, E501
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos: int = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            result.extend(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            if not parsed.success:
                break
            pos = parsed.position

        if pos != len(target):
            return Failure("parse error.", pos)

        return Success(result, pos)

    return Parser(f)


def sepBy(parser: Parser, sep: Parser) -> Parser:
    r"""Parse zero or more occurrences of parser, separated by sep. Returns a list of values returned by parser.

    Example
    -------
    >>> from simpleparser import token, regex, sepBy
    >>> sepBy(regex('\w*'), token(',')).exec('hoge,hoge')
    ['hoge', 'hoge']
    """  # noqa: D401, E501
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            result.extend(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            if not parsed.success:
                break
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def lazy(callback: Callable[[], Parser]) -> Parser:
    """Lazy function.

    Example
    -------
    >>> from simpleparser import token, seq, option
    >>> parse = option(seq(token('hoge'), lazy(lambda: parse)))
    >>> parse.exec('hoge', 0)
    ['hoge']
    >>> parse.exec('hogehoge', 0)
    ['hoge', 'hoge']
    >>> parse.exec('hogehogehoge', 0)
    ['hoge', 'hoge', 'hoge']
    """
    def f(target: str, position: int) -> ParseResult:
        parse = callback()
        return parse.exec(target, position)

    return Parser(f)


def map(parser: Parser, selector: Callable[[List[str]], List[str]]) -> Parser:
    """Map function.

    Example
    -------
    >>> from simpleparser import token, map
    >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0)
    ['foo aaa']
    """  # noqa: E501
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
