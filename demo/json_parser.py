# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import simple_parser as p


class json_parser:
    '''
    Example
    -------
    >>> p = json_parser()
    >>> p.parse("{}").result()
    ['{', '}']
    >>> p.parse("{p1:1}").result()
    ['{', 'p1', ':', 1, '}']
    >>> p.parse("{p2:'a'}").result()
    ['{', 'p2', ':', 'a', '}']
    >>> p.parse("{p1:1,p2:'a',p3:[]}").result()
    '''
    def parse(self, s):

        propName = p.regex("\w+")
        colon = p.token(":")
        p_str = (p.token('"') + p.regex("\w*") + p.token('"')) | (p.token("'") + p.regex("\w*") + p.token("'"))
        num = p.regex("\d+").map(lambda x: int(float("".join(x))) if "".join(x) != "" else x)
        ary = p.token("[") + p.token("]")

        parser = p.token("{") + p.sepBy(propName + colon + (num | p_str), p.token(",")) + p.token("}")

        return parser.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
