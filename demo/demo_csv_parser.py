"""csv parsing sample."""

from typing import List
from simpleparser import (
    token, sep_by, end_by, transform, seq, many, choice, none_of,
    ParseResult
)
from simpleparser.builtin_parsers import newline


class CsvParser():
    r"""parse_csv.

    http://book.realworldhaskell.org/read/using-parsec.html

    Example
    -------
    >>> p = CsvParser()
    >>> p.parse("hi")
    parse error at (0): unexpected hi expecting  (by transform)
    >>>
    >>> p.parse('"hi",\n')
    [['"hi"']]
    >>>
    >>> p.parse('"line1"\n"line2"\n"line3"\n')
    [['"line1"'], ['"line2"'], ['"line3"']]
    >>>
    >>> p.parse('"cell1","cell2","cell3"\n')
    [['"cell1"', '"cell2"', '"cell3"']]
    >>>
    >>> p.parse('"l1c1","l1c2"\n"l2c1","l2c2"\n')
    [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    >>>
    # >>> p.parse('Hi,\n\n,Hello\n')
    # [['Hi', ''], [''], ['', 'Hello']]
    # >>>
    >>> p.parse('line1\r\nline2\nline3\n\rline4\rline5\n')
    [['line1'], ['line2'], ['line3'], ['line4'], ['line5']]
    >>>
    >>> p.parse("\"This, is, one, big, cell\n")
    parse error at (0): unexpected "This expecting  (by transform)
    >>>
    >>> p.parse('"Cell without an end\n')
    parse error at (0): unexpected "Cell expecting  (by transform)
    >>> s = '"Product","Price"\n"O\'Reilly Socks",10\n"Shirt with ""Haskell"" text",20\n"Shirt, ""O\'Reilly"" version",20\n"Haskell Caps",15\n'  # noqa E501
    >>> p.parse(s)
    [['"Product"', '"Price"'], ['"O\'Reilly Socks"', '10'], ['"Shirt with ""Haskell"" text"', '20'], ['"Shirt, ""O\'Reilly"" version"', '20'], ['"Haskell Caps"', '15']]
    """  # noqa E501

    def parse(self, s: str) -> ParseResult:
        """Parse method."""

        dq = token('"')
        assert dq.exec('"foo"').tokens == ['"']

        dq_escaped = token('""')

        chars = transform(many(choice(dq_escaped, none_of('",\n\r'))), lambda x: ["".join(x)])  # noqa E501
        assert chars.exec("cell1,cell2").tokens[0] == 'cell1'  # noqa E501

        quoted_chars = transform(seq(dq, many(choice(dq_escaped, none_of('"'))), dq), lambda x: ["".join(x)])  # noqa E501
        assert quoted_chars.exec('"ce ""ll"" 1",cell2').tokens[0] == '"ce ""ll"" 1"'  # noqa E501

        cell = transform(choice(quoted_chars, chars), lambda x: ["".join(x)])  # noqa E501
        assert cell.exec('"ce ""ll"" 1",cell2').tokens == ['"ce ""ll"" 1"']  # noqa E501
        assert cell.exec('cell1,cell2').tokens == ['cell1']  # noqa E501

        def line_selector(x: List[str]) -> List[List[str]]:
            if len(x) == 0:
                return []
            if x is None:
                return []
            return [x]

        line = transform(sep_by(cell, token(',')), line_selector)  # noqa E501
        assert line.exec('"ce ""ll"" 1",cell2').tokens == [['"ce ""ll"" 1"', "cell2"]], line.exec('"ce ""ll"" 1",cell2')  # noqa E501

        eol = choice(seq(token("\n"), token("\r")), newline())
        # eol = choice(token("\n"), token("\r"))
        # eol = token("\n")
        assert eol.exec("\n").tokens == ["\n"]
        assert eol.exec("\nline2").tokens == ["\n"]
        assert eol.exec('123456789\nline2\n', 9).tokens == ["\n"], eol.exec('123456789\nline2\n', 9)
        assert eol.exec('"ce ""ll"" 1",cell2\nline2\n', 19).tokens == ["\n"], eol.exec('"ce ""ll"" 1",cell2\nline2\n', 19)
        assert eol.exec('"ce ""ll"" 1",cell2\nline2\n', 25).tokens == ["\n"], eol.exec('"ce ""ll"" 1",cell2\nline2\n', 25)
        parser = end_by(line, eol)
        assert parser.exec('"ce ""ll"" 1",cell2\nline2\n').tokens == [['"ce ""ll"" 1"', "cell2"], ["line2"]]  # noqa E501
        # s = '"Product","Price"\n"O\'Reilly Socks",10\n"Shirt with ""Haskell"" text",20\n"Shirt ""O\'Reilly"" version",20\n"Haskell Caps",15\n'  # noqa E501
        # tmp = parser.exec(s)
        # assert tmp.tokens == [["Product","Price"],["O'Reilly Socks","10"],["Shirt with \"Haskell\" text","20"],["Shirt, \"O'Reilly\" version","20"],["Haskell Caps","15"]], tmp  # noqa E501

        return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
