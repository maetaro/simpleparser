"""csv parsing sample."""

from typing import List
from simpleparser import (
    token, sep_by, end_by, transform, seq, many, choice, regex, option, none_of,
    ParseResult
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
    # >>>
    # >>> p.parse(r'"hi"\n')
    # [['"hi"']]
    # >>>
    # >>> p.parse(r'"line1"\n"line2"\n"line3"\n')
    # [['"line1"'], ['"line2"'], ['"line3"']]
    # >>>
    # >>> p.parse(r'"cell1","cell2","cell3"\n')
    # [['"cell1"', '"cell2"', '"cell3"']]
    # >>>
    # >>> p.parse(r'"l1c1","l1c2"\n"l2c1","l2c2"\n')
    # [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    # >>>
    # >>> p.parse(r'Hi,\n\n,Hello\n')
    # [['Hi', ''], [''], ['', 'Hello']]
    # >>>
    # >>> p.parse(r'line1\r\nline2\nline3\n\rline4\rline5\n')
    # [['line1'], ['line2'], ['line3'], ['line4'], ['line5']]
    # >>>
    # >>> p.parse(r"\"This, is, one, big, cell\"\n")
    # >>>
    # >>> p.parse(r'"Cell without an end\n')
    # parse error at (0): unexpected "Cell expecting  (by transform)
    # >>> s = r'"Product","Price"\n"O\'Reilly Socks",10\n"Shirt with ""Haskell"" text",20\n"Shirt, ""O\'Reilly"" version",20\n"Haskell Caps",15'
    # >>> print(s)
    # >>> p.parse(s)
    # [["Product","Price"],["O'Reilly Socks","10"],["Shirt with \"Haskell\" text","20"],["Shirt, \"O'Reilly\" version","20"],["Haskell Caps","15"]]
    """

    def parse(self, s: str) -> ParseResult:
        """Parse method."""
        def line_selector(x: List[str]) -> List[List[str]]:
            if len(x) == 0:
                return []
            if x is None:
                return []
            return [x]

        dq = token('"')
        chars = regex(r"\w*")
        quoted_chars = seq(dq, many(none_of('""')), dq)
        cell = transform(choice(quoted_chars, chars), lambda x: ["".join(x)])  # noqa E501
        line = transform(sep_by(cell, token(',')), line_selector)
        eol = choice(seq(token(r"\n"), token(r"\r")), newline())
        parser = end_by(line, eol)

        return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
