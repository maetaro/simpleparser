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
    name: str = f"token {s}"

    def f(self: PrimitiveParser, target: str,
          position: int = 0) -> ParseResult:
        if target[position:position + length] == s:
            return Success([s], position + length, name=name)
        msg = (f"parse error at ({position}):"
               f" unexpected {target[position:position + length]}"
               f" expecting {s} (by {self.parser_type})")
        return Failure(msg, position, name=name)

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
    name: str = f"regex {pattern}"
    def f(self: PrimitiveParser, target: str,
          position: int = 0) -> ParseResult:
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()), name=name)
        msg = (f"parse error at ({position}):"
               f" unexpected {target[position:position + 5]}"
               f" expecting {pattern} (by {self.parser_type})")
        return Failure(msg, position, name=name)

    return PrimitiveParser(f, pattern)


# def char() -> Parser:
#     """Char function."""
#     return regex(r"\S")


def none_of(s: str) -> Parser:
    """none_of function.

    As the dual of oneOf, none_of(cs) succeeds if the current character
    not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
    >>> from simpleparser import none_of, choice, token, many, transform, seq
    >>> p = none_of("abcdefg")
    >>> p.exec("hello")
    ['h']
    >>> chars = choice(token('""'), none_of('",'))
    >>> p = transform(many(chars), lambda x: ["".join(x)])
    >>> text = r'Shirt with ""Haskell"" text'
    >>> p.exec(text)
    ['Shirt with ""Haskell"" text']
    >>> dq = token('"')
    >>> p2 = transform(seq(dq, p, dq), lambda x: ["".join(x)])
    >>> text = r'"Shirt with ""Haskell"" text"'
    >>> p2.exec(text)
    ['"Shirt with ""Haskell"" text"']
    """  # noqa: E501
    name: str = f"none_of {s}"

    def f(target: str, position: int = 0) -> ParseResult:
        exists: bool = False
        targetChar: str = target[position:position + 1]
        for c in s:
            if targetChar == c:
                exists = True
                break
        if not exists:
            return Success([targetChar], position + 1, name=name)
        return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position, name=name)  # noqa: E501

    return Parser(f)


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
