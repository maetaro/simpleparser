"""csv parsing sample."""

from simpleparser import (
    token, regex, choice, seq, lazy, sep_by, option, transform,
    ParseResult, Parser
)


class json_parser:
    """Json parser.

    Example
    -------
    >>> p = json_parser()
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
        propName: Parser = regex(r"\w+")
        colon: Parser = token(":")
        sq: Parser = token("'")
        dq: Parser = token('"')
        p_str: Parser = transform(choice(seq(dq, regex(r"\w*"), dq), seq(sq, regex(r"\w*"), sq)), lambda x: ["".join(x)])  # noqa: E501
        num: Parser = transform(regex(r"\d+"), lambda x: [str(int(float("".join(x))))] if "".join(x) != "" else x)  # noqa: E501
        p_multi: Parser = choice(num, p_str, lazy(lambda: obj), lazy(lambda: ary))
        ary: Parser = seq(token("["), option(sep_by(p_multi, token(","))), token("]"))  # noqa: E501
        obj: Parser = seq(token("{"), option(sep_by(seq(propName, colon, p_multi), token(","))), token("}"))  # noqa: E501

        if s.lstrip()[0] == '[':
            return ary.exec(s, 0)
        else:
            return obj.exec(s, 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
