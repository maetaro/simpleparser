"""a simple parser combinator."""

import re
from typing import Callable
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def token(s: str) -> Parser:
    """Token function.

    Example
    -------
    >>> token("foo").exec("foobar")
    ['foo']
    >>> token("bar").exec("foobar")
    parse error at (0): unexpected foo expecting bar
    """
    length: int = len(s)

    def f(target: str, position: int = 0) -> ParseResult:
        if target[position:position + length] == s:
            return Success([s], position + length)
        msg = ("parse error at (" + str(position) + "):"
               " unexpected " + target[position:position + length] + ""
               " expecting " + s + "")
        return Failure(msg, position)

    return Parser(f)


def regex(pattern: str) -> Parser:
    """Regex function returns a function that parses the beginning of the received string with the regular expression pattern.

    Parameters
    ----------
    pattern: str
        a regular expression string.
    Example
    -------
    >>> parser = regex("hoge")
    >>> parser.exec('hoge', 0)
    ['hoge']
    >>> parser = regex("([1-9][0-9]*)")
    >>> parser.exec('2014a', 0)
    ['2014']
    >>> parser.exec('01', 0)
    parse error at (0): unexpected 01 expecting ([1-9][0-9]*)
    """  # noqa: E501
    def f(target: str, position: int = 0) -> ParseResult:
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()))
        msg = ("parse error at (" + str(position) + "):"
               " unexpected " + target[position:] + ""
               " expecting " + pattern + "")
        return Failure(msg, position)

    return Parser(f)


def noneOf(s: str) -> Parser:
    """
    As the dual of oneOf, noneOf cs succeeds if the current character not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
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


def char(s: str) -> Parser:
    """Char function."""
    return token(s)


def endBy(parser: Parser, sep: Parser) -> Parser:
    r"""Endby p sep parses zero or more occurrences of p, separated and ended by sep.

    Returns a list of values returned by p.

    Example
    -------
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
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
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
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            if not parsed.success:
                break
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def many(parser: Parser) -> Parser:
    """Many function.

    Example
    -------
    >>> many(token('hoge')).exec('hogehoge')
    ['hoge', 'hoge']
    >>> many(token('hoge')).exec('', 0)
    []
    >>> many(token('foobar')).exec('foo', 0)
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def choice(*args) -> Parser:
    """Choice function.

    Example
    -------
    >>> parse = many(choice(token('hoge'), token('fuga')))
    >>> parse.exec('', 0)
    []
    >>> parse.exec('hogehoge', 0)
    ['hoge', 'hoge']
    >>> parse.exec('fugahoge', 0)
    ['fuga', 'hoge']
    >>> parse.exec('fugafoo', 0)
    ['fuga']
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


def seq(*args) -> Parser:
    r"""Seq function.

    Example
    -------
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
        result = []
        pos_org = position
        for parser in parsers:
            parsed = parser.exec(target, position)
            if not parsed.success:
                return Failure(parsed.message, pos_org)
            if parsed.tokens is None:
                continue
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            position = parsed.position

        return Success(result, position)

    return Parser(f)


def option(parser: Parser) -> Parser:
    """Option function.

    Example
    -------
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


def lazy(callback: Callable[[], Parser]) -> Parser:
    """Lazy function.

    Example
    -------
    >>> parse = option(seq(token('hoge'), lazy(lambda: parse)))
    >>> parse.exec('hoge', 0)
    ['hoge']
    >>> parse.exec('hogehoge', 0)
    ['hoge', 'hoge']
    >>> parse.exec('hogehogehoge', 0)
    ['hoge', 'hoge', 'hoge']
    """
    def f(target, position) -> ParseResult:
        parse = callback()
        return parse.exec(target, position)

    return Parser(f)


def map(parser: Parser, selector) -> Parser:
    """Map function.

    Example
    -------
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
