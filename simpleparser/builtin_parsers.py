"""a simple parser combinator."""

from simpleparser import token, seq, transform, choice, Parser


def lf() -> Parser:
    r"""Return a LF parser.

    Returns
    -------
        Parser: LF(\n) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import lf
    >>> p = lf()
    >>> p.exec("\nfoo")
    ['\n']
    """
    return token("\n")


def cr() -> Parser:
    r"""Return a CR parser.

    Returns
    -------
        Parser: CR(\r) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import cr
    >>> p = cr()
    >>> p.exec("\rfoo")
    ['\r']
    """
    return token("\r")


def crlf() -> Parser:
    r"""Return a CRLF parser.

    Returns
    -------
        Parser: CRLF(\r\n) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import crlf
    >>> p = crlf()
    >>> p.exec("\r\nfoo")
    ['\r\n']
    """
    return transform(seq(cr(), lf()), lambda x: ["".join(x)])


def newline() -> Parser:
    r"""Return a new line parser.

    Returns
    -------
        Parser: CRLF(\r\n) or CR(\r) or LF(\n) parser.

    Example
    -------
    >>> from simpleparser.builtin_parsers import newline
    >>> p = newline()
    >>> p.exec("\r\nfoo")
    ['\r\n']
    >>> p.exec("\rfoo")
    ['\r']
    >>> p.exec("\nfoo")
    ['\n']
    """
    return choice(crlf(), cr(), lf())


# TODO: def char() -> Parser:
# TODO:     """Char function."""
# TODO:     return regex(r"\S")


# TODO: def noneOf(s: str) -> Parser:
# TODO:     """
# TODO:     As the dual of oneOf, noneOf cs succeeds
# TODO:     if the current character not in the supplied
# TODO:     list of characters cs. Returns the parsed character.
# TODO:
# TODO:     Example
# TODO:     -------
# TODO:     >>> from simpleparser import noneOf
# TODO:     >>> noneOf("abcdefg").exec("hello", 0)
# TODO:     ['h']
# TODO:     """  # noqa: E501
# TODO:     def f(target: str, position: int = 0) -> ParseResult:
# TODO:         exists: bool = False
# TODO:         targetChar: str = target[position:position + 1]
# TODO:         for c in s:
# TODO:             if targetChar == c:
# TODO:                 exists = True
# TODO:                 break
# TODO:         if not exists:
# TODO:             return Success([targetChar], position + 1)
# TODO:         return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)  # noqa: E501
# TODO:
# TODO:     return Parser(f)
