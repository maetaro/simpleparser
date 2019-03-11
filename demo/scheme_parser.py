# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..\src'))

import simple_parser as p


class schemeparser:
    """
    >>> parser = schemeparser()
    >>> parser.parse("( + 1 7 )").result()
    [True, ['(', '+', ' ', '1', ' ', '7', ')'], 7]
    >>> parser.parse("( + 1 ( - 2 3 ) )").result()
    [True, ['(', '+', ' ', '1', ' ', '(', ' ', '-', ' ', '2', ' ', '3', ')', ')'], 13]
    >>> parser.parse("( + 1 ( - 2 ( + 3 4 ) ) )").result()
    [True, ['(', '+', ' ', '1', ' ', '(', ' ', '-', ' ', '2', ' ', '3', ')', ')'], 13]
    """
    def parse(self, s):
        l_paren = p.token("(")
        r_paren = p.token(")")
        symbol = p.regex("\S")
        blank = p.regex("\s")
        opt_blank = p.option(blank)

        #operator = symbol
        #num = symbol
        #parenthesis = p.lazy(lambda: p.seq(l_paren, expression, r_paren))
        #atom = p.choice(num, parenthesis)
        #expression = p.seq(atom, p.many(p.seq(operator, atom)))
        #parser = expression

        exp = p.lazy(lambda:
                     p.seq(l_paren,
                           blank,
                           symbol,
                           p.many(
                               p.seq(blank, p.choice(symbol, exp), blank)
                               ),
                           blank,
                           r_paren)
                     )
        parser = exp
        return parser(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
