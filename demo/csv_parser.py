# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..\src'))

import simple_parser as p


class csv_parser:
    '''
    http://book.realworldhaskell.org/read/using-parsec.html

    Example
    -------
    >>> parseCSV = csv_parser()
    >>> parseCSV.parse("hi")
    "Left \"(unknown)\" (line 1, column 3):"
    "unexpected end of input"
    "expecting \",\" or \"\\n""
    >>> parseCSV.parse("hi\\n")
    [["hi"]]
    >>> parseCSV.parse("line1\\nline2\\nline3\\n")
    [["line1"],["line2"],["line3"]]
    >>> parseCSV.parse("cell1,cell2,cell3\\n")
    [["cell1","cell2","cell3"]]
    >>> parseCSV.parse("l1c1,l1c2\\nl2c1,l2c2\\n")
    [["l1c1","l1c2"],["l2c1","l2c2"]]
    '''
    def parse(self, s):

        dquote = p.token("\"")
        quotedChar = p.choice(p.noneOf(dquote), p.option("\"\""))
        quotedCell = p.seq(p.token("("), quotedChar, p.token(")"))
        cell = p.choice(quotedCell, p.many(p.noneOf(",\n\r")))
        line = p.sepBy(cell, (p.char(',')))
        eol = p.choice(p.token("\n\r"), p.token("\r\n"), p.token("\n"), p.token("\r"))

        #parser = p.endBy(line, eol)
        parser = p.sepBy(line, eol)

        #parseCSV :: String -> Either ParseError [[String]]
        #parseCSV input = parse csvFile "(unknown)" input

        #main =
        #    do c <- getContents
        #       case parse csvFile "(stdin)" c of
        #            Left e -> do putStrLn "Error parsing input:"
        #                         print e
        #            Right r -> mapM_ print r

        return parser(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
