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
