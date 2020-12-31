"""csv parsing sample."""

from simpleparser import (
    token, regex, choice, seq, lazy, sep_by, option, transform,
    ParseResult
)


class JsonParser:
    """Json parser.

    Example
    -------
    >>> p = JsonParser()
    >>> p.parse("{}")
    ['{', '}']
    >>> p.parse("{p1:1,p2:2}")
    ['{', 'p1', ':', '1', 'p2', ':', '2', '}']
    >>> p.parse("{p1:1,p2:{p1:1}}")
    ['{', 'p1', ':', '1', 'p2', ':', '{', 'p1', ':', '1', '}', '}']
    >>> p.parse("[[1,2,3],[2],[3]]")
    ['[', '[', '1', '2', '3', ']', '[', '2', ']', '[', '3', ']', ']']
    >>> p.parse("[1,2,3]")
    ['[', '1', '2', '3', ']']
    >>> p.parse("{p2:'a'}")
    ['{', 'p2', ':', "'a'", '}']
    >>> p.parse("{p1:1,p2:'a',p3:[]}")
    ['{', 'p1', ':', '1', 'p2', ':', "'a'", 'p3', ':', '[', ']', '}']
    """

    def parse(self, s: str) -> ParseResult:
        """Parse method."""
        propName = regex(r"\w+")
        colon = token(":")
        sq = token("'")
        dq = token('"')
        p_str = transform(choice(seq(dq, regex(r"\w*"), dq), seq(sq, regex(r"\w*"), sq)), lambda x: ["".join(x)])  # noqa: E501
        num = transform(regex(r"\d+"), lambda x: [str(int(float("".join(x))))] if "".join(x) != "" else x)  # noqa: E501
        p_multi = choice(num, p_str, lazy(lambda: obj), lazy(lambda: ary))
        ary = seq(token("["), option(sep_by(p_multi, token(","))), token("]"))  # noqa: E501
        obj = seq(token("{"), option(sep_by(seq(propName, colon, p_multi), token(","))), token("}"))  # noqa: E501

        if s.lstrip()[0] == '[':
            return ary.exec(s, 0)
        else:
            return obj.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
