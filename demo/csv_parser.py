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
    >>> p = csv_parser()
    >>> p.parse("hi").result()
    "Left \"(unknown)\" (line 1, column 3):"
    "unexpected end of input"
    "expecting \",\" or \"\\n""
    >>> p.parse('"hi"\\n').result()
    [['"hi"']]
    >>> p.parse('"line1"\\n"line2"\\n"line3"\\n').result()
    [['"line1"'],['"line2"'],['"line3"']]
    >>> p.parse('"cell1","cell2","cell3"\\n').result()
    [['"cell1"', '"cell2"', '"cell3"']]
    >>> p.parse('"l1c1","l1c2"\\n"l2c1","l2c2"\\n').result()
    [['"l1c1"', '"l1c2"'], ['"l2c1"', '"l2c2"']]
    '''
    def parse(self, s):

        dquote = p.token("\"")
        cell = p.map(p.seq(dquote, p.regex("\w*"), dquote), lambda x: "".join(x))
        line = p.map(p.sepBy(cell, p.char(',')), lambda x: [x])
        newLine = (p.token("\n\r") | p.token("\r\n") | p.token("\n") | p.token("\r"))
        lines = p.sepBy(cell, newLine)
        eol = p.choice(p.token("\n\r"), p.token("\r\n"), p.token("\n"), p.token("\r"))

        parser = p.endBy(line, eol)
        #parser = line # p.sepBy(line, eol)

        #parseCSV :: String -> Either ParseError [[String]]
        #parseCSV input = parse csvFile "(unknown)" input

        #main =
        #    do c <- getContents
        #       case parse csvFile "(stdin)" c of
        #            Left e -> do putStrLn "Error parsing input:"
        #                         print e
        #            Right r -> mapM_ print r

        return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
