"""a simple parser combinator."""

import re
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def token(s: str) -> Parser:
    """Token function.

    Parameters
    ----------
    s: str
        a literal string.

    Example
    -------
    >>> from simpleparser import token
    >>> foo = token("foo")
    >>> foo.exec("foobar")
    ['foo']
    >>> foo.exec("alice")
    parse error at (0): unexpected ali expecting foo
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


def char() -> Parser:
    """Char function."""
    return regex(r"\S")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
