# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import simple_parser as p


def parseCsv(s):
    '''
    http://book.realworldhaskell.org/read/using-parsec.html

    Example
    -------
    >>> p = parseCsv
    >>> p("hi").result()
    "Left \"(unknown)\" (line 1, column 3):"
    "unexpected end of input"
    "expecting \",\" or \"\\n""
    >>> p('"hi"\\n').result()
    [['"hi"']]
    >>> p('"line1"\\n"line2"\\n"line3"\\n').result()
    [['"line1"'], ['"line2"'], ['"line3"']]
    >>> p('"cell1","cell2","cell3"\\n').result()
    [['"cell1"', '"cell2"', '"cell3"']]
    >>> p('"l1c1","l1c2"\\n"l2c1","l2c2"\\n').result()
    [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    >>> p("line1\\r\\nline2\\nline3\\n\\rline4\\rline5\\n").result()
    [["line1"], ["line2"], ["line3"], ["line4"], ["line5"]]
    '''

    def line_selector(x):
        if len(x) == 0:
            return []
        if x is None:
            return []
        return [x]

    dquote = p.token("\"")
    cell = (dquote + p.regex("\w*") + dquote).map(lambda x: "".join(x))
    line = p.sepBy(cell, p.char(',')).map(line_selector)
    eol = p.token("\n\r") | p.token("\r\n") | p.token("\n") | p.token("\r")

    parser = p.endBy(line, eol)

    return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
