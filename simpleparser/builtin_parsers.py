"""a simple parser combinator."""

from simpleparser.parser import Parser
from simpleparser import token, seq, transform


def lf() -> Parser:
    r"""Return a LF parser.

    Returns
    -------
        Parser: LF(\n) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import lf
    >>> p = lf()
    >>> p.exec(r"\nfoo")
    ['\\n']
    >>> p.exec("foo")
    parse error at (0): unexpected fo expecting \n (by token)
    """
    return token(r"\n")


def cr() -> Parser:
    r"""Return a CR parser.

    Returns
    -------
        Parser: CR(\r) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import cr
    >>> p = cr()
    >>> p.exec(r"\rfoo")
    ['\\r']
    >>> p.exec("foo")
    parse error at (0): unexpected fo expecting \r (by token)
    """
    return token(r"\r")


def crlf() -> Parser:
    r"""Return a CRLF parser.

    Returns
    -------
        Parser: CRLF(\r\n) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import crlf
    >>> p = crlf()
    >>> p.exec(r"\r\nfoo")
    ['\\r\\n']
    >>> p.exec("foo")
    parse error at (0): unexpected fo expecting \r (by token)
    """
    return transform(seq(cr(), lf()), lambda x: ["".join(x)])


# def char() -> Parser:
#     """Char function."""
#     return regex(r"\S")


# def noneOf(s: str) -> Parser:
#     """
#     As the dual of oneOf, noneOf cs succeeds
#     if the current character not in the supplied
#     list of characters cs. Returns the parsed character.
#
#     Example
#     -------
#     >>> from simpleparser import noneOf
#     >>> noneOf("abcdefg").exec("hello", 0)
#     ['h']
#     """  # noqa: E501
#     def f(target: str, position: int = 0) -> ParseResult:
#         exists: bool = False
#         targetChar: str = target[position:position + 1]
#         for c in s:
#             if targetChar == c:
#                 exists = True
#                 break
#         if not exists:
#             return Success([targetChar], position + 1)
#         return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)  # noqa: E501
#
#     return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
