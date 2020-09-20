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
    >>> p.parse("{p1:1,p2:2}").result()
    ['{', 'p1', ':', 1, 'p2', ':', 2, '}']
    >>> p.parse("{p1:1,p2:{p1:1,p2:2}}").result()
    ['{', 'p1', ':', 1, 'p2', ':', '{', 'p1', ':', 1, 'p2', ':', 2, '}', '}']
    >>> p.parse("[[1,2,3],[2],[3]]").result()
    ['[', '[', 1, 2, 3, ']', '[', 2, ']', '[', 3, ']', ']']
    >>> p.parse("[1,2,3]").result()
    ['[', 1, 2, 3, ']']
    >>> p.parse("{p2:'a'}").result()
    ['{', 'p2', ':', "'a'", '}']
    >>> p.parse("{p1:1,p2:'a',p3:[]}").result()
    ['{', 'p1', ':', 1, 'p2', ':', "'a'", 'p3', ':', '[', ']', '}']
    '''
    def parse(self, s):
        propName = p.regex("\w+")
        colon = p.token(":")
        sq = p.token("'")
        dq = p.token('"')
        p_str = ((dq + p.regex("\w*") + dq) | (sq + p.regex("\w*") + sq)).map(lambda x: "".join(x))
        num = p.regex("\d+").map(lambda x: int(float("".join(x))) if "".join(x) != "" else x)
        p_multi = num | p_str | p.lazy(lambda: obj) | p.lazy(lambda: ary)
        ary = p.token("[") + p.option(p.sepBy(p_multi, p.token(","))) + p.token("]")
        obj = p.token("{") + p.option(p.sepBy(propName + colon + p_multi, p.token(","))) + p.token("}")

        if s.lstrip()[0] == '[':
            return ary.exec(s, 0)
        else:
            return obj.exec(s, 0)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
