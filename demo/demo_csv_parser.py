"""csv parsing sample."""

from typing import List
from simpleparser import (
    token, ParseResult, sep_by, end_by, transform, seq, regex
)
from simpleparser.builtin_parsers import newline


class CsvParser():
    r"""parse_csv.

    http://book.realworldhaskell.org/read/using-parsec.html

    Example
    -------
    # >>> p = CsvParser()
    # >>> p.parse("hi")
    # parse error at (0): unexpected hi expecting  (by transform)
    # >>> p.parse('"hi"\n')
    # ['"hi"']
    # >>> p.parse('"line1"\\n"line2"\\n"line3"\\n')
    # [['"line1"'], ['"line2"'], ['"line3"']]
    # >>> p.parse('"cell1","cell2","cell3"\\n')
    # [['"cell1"', '"cell2"', '"cell3"']]
    # >>> p.parse('"l1c1","l1c2"\\n"l2c1","l2c2"\\n')
    # [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    # >>> p.parse("line1\\r\\nline2\\nline3\\n\\rline4\\rline5\\n")
    # [["line1"], ["line2"], ["line3"], ["line4"], ["line5"]]
    """

    def parse(self, s: str) -> ParseResult:
        """Parse method."""
        def line_selector(x: List[str]) -> List[str]:
            if len(x) == 0:
                return []
            if x is None:
                return []
            return x

        dquote = token('"')
        cell = transform(seq(dquote, regex(r"\w*"), dquote), lambda x: ["".join(x)])  # noqa F501
        line = transform(sep_by(cell, token(',')), line_selector)
        eol = newline()

        parser = end_by(line, eol)

        return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
