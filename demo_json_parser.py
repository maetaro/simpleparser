"""csv parsing sample."""

import simpleparser as p


class json_parser:
    """Json parser.

    Example
    -------
    >>> p = json_parser()
    >>> p.parse("{}")
    ['{', '}']
    >>> p.parse("{p1:1,p2:2}")
    ['{', 'p1', ':', 1, 'p2', ':', 2, '}']
    >>> p.parse("{p1:1,p2:{p1:1,p2:2}}")
    ['{', 'p1', ':', 1, 'p2', ':', '{', 'p1', ':', 1, 'p2', ':', 2, '}', '}']
    >>> p.parse("[[1,2,3],[2],[3]]")
    ['[', '[', 1, 2, 3, ']', '[', 2, ']', '[', 3, ']', ']']
    >>> p.parse("[1,2,3]")
    ['[', 1, 2, 3, ']']
    >>> p.parse("{p2:'a'}")
    ['{', 'p2', ':', "'a'", '}']
    >>> p.parse("{p1:1,p2:'a',p3:[]}")
    ['{', 'p1', ':', 1, 'p2', ':', "'a'", 'p3', ':', '[', ']', '}']
    """

    def parse(self, s):
        """Parse method."""
        propName = p.regex(r"\w+")
        colon = p.token(":")
        sq = p.token("'")
        dq = p.token('"')
        p_str = ((dq + p.regex(r"\w*") + dq) | (sq + p.regex(r"\w*") + sq)).map(lambda x: "".join(x))  # noqa: E501
        num = p.regex(r"\d+").map(lambda x: int(float("".join(x))) if "".join(x) != "" else x)  # noqa: E501
        p_multi = num | p_str | p.lazy(lambda: obj) | p.lazy(lambda: ary)
        ary = p.token("[") + p.option(p.sepBy(p_multi, p.token(","))) + p.token("]")  # noqa: E501
        obj = p.token("{") + p.option(p.sepBy(propName + colon + p_multi, p.token(","))) + p.token("}")  # noqa: E501

        if s.lstrip()[0] == '[':
            return ary.exec(s, 0)
        else:
            return obj.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
