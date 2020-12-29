"""csv parsing sample."""

from typing import List
import simpleparser as p


def parseCsv(s: str) -> p.ParseResult:
    r"""Parsecsv.

    http://book.realworldhaskell.org/read/using-parsec.html

    # TODO: doctest
    # Example
    # -------
    # >>> p = parseCsv
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

    dquote = p.token("\"")
    cell = p.map(p.seq(dquote, p.regex(r"\w*"), dquote), lambda x: ["".join(x)])  # noqa F501
    line = p.map(p.sepBy(cell, p.char(',')), line_selector)
    eol = p.choice(p.token("\n\r"), p.token("\r\n"), p.token("\n"), p.token("\r"))  # noqa F501

    parser = p.endBy(line, eol)

    return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
