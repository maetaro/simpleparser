"""csv parsing sample."""

from typing import List
from simpleparser import token, ParseResult, sepBy, end_by, transform, seq, regex, choice


def parse_csv(s: str) -> ParseResult:
    r"""parse_csv.

    http://book.realworldhaskell.org/read/using-parsec.html

    # TODO: doctest
    # Example
    # -------
    # >>> p = parse_csv
    # >>> p("hi").result()
    # "Left \"(unknown)\" (line 1, column 3):"
    # "unexpected end of input"
    # "expecting \",\" or \"\\n""
    # >>> p('"hi"\\n').result()
    # [['"hi"']]
    # >>> p('"line1"\\n"line2"\\n"line3"\\n').result()
    # [['"line1"'], ['"line2"'], ['"line3"']]
    # >>> p('"cell1","cell2","cell3"\\n').result()
    # [['"cell1"', '"cell2"', '"cell3"']]
    # >>> p('"l1c1","l1c2"\\n"l2c1","l2c2"\\n').result()
    # [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    # >>> p("line1\\r\\nline2\\nline3\\n\\rline4\\rline5\\n").result()
    # [["line1"], ["line2"], ["line3"], ["line4"], ["line5"]]
    """

    def line_selector(x: List[str]) -> List[str]:
        if len(x) == 0:
            return []
        if x is None:
            return []
        return x

    dquote = token('"')
    cell = transform(seq(dquote, regex(r"\w*"), dquote), lambda x: ["".join(x)])  # noqa F501
    line = transform(sepBy(cell, token(',')), line_selector)
    eol = choice(token("\n\r"), token("\r\n"), token("\n"), token("\r"))  # noqa F501

    parser = end_by(line, eol)

    return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
