"""a simple parser combinator."""

import re
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser, PrimitiveParser


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
    parse error at (0): unexpected ali expecting foo (by token)
    """
    length: int = len(s)
    assert length > 0, ""

    def f(self: PrimitiveParser, target: str,
          position: int = 0) -> ParseResult:
        if target[position:position + length] == s:
            return Success([s], position + length)
        msg = (f"parse error at ({position}):"
               f" unexpected {target[position:position + length]}"
               f" expecting {s} (by {self.parser_type})")
        return Failure(msg, position)

    return PrimitiveParser(f, s)


def regex(pattern: str) -> Parser:
    """Regex function.

    Returns a function that parses the beginning of the
    received string with the regular expression pattern.

    Parameters
    ----------
    pattern: str
        a regular expression string.

    Example
    -------
    >>> from simpleparser import regex
    >>> num = regex("([1-9][0-9]*)")
    >>> num.exec('2014a')
    ['2014']
    >>> num.exec('abc')
    parse error at (0): unexpected abc expecting ([1-9][0-9]*) (by regex)
    """
    def f(self: PrimitiveParser, target: str,
          position: int = 0) -> ParseResult:
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()))
        msg = (f"parse error at ({position}):"
               f" unexpected {target[position:position + 5]}"
               f" expecting {pattern} (by {self.parser_type})")
        return Failure(msg, position)

    return PrimitiveParser(f, pattern)


# def char() -> Parser:
#     """Char function."""
#     return regex(r"\S")


def none_of(s: str) -> Parser:
    """As the dual of oneOf, noneOf cs succeeds

    if the current character not in the supplied
    list of characters cs. Returns the parsed character.

    Example
    -------
    >>> from simpleparser import none_of
    >>> p = none_of("abcdefg")
    >>> p.exec("hello")
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
