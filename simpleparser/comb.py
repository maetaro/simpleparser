"""a simple parser combinator."""

from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def many(parser: Parser) -> Parser:
    """Many function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> many(token('hoge')).exec('hogehoge')
    ['hoge', 'hoge']
    >>> many(token('hoge')).exec('', 0)
    []
    >>> many(token('foobar')).exec('foo', 0)
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def choice(*args) -> Parser:
    """Choice function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> parse = many(choice(token('hoge'), token('fuga')))
    >>> parse.exec('', 0)
    []
    >>> parse.exec('hogehoge', 0)
    ['hoge', 'hoge']
    >>> parse.exec('fugahoge', 0)
    ['fuga', 'hoge']
    >>> parse.exec('fugafoo', 0)
    ['fuga']
    """
    parsers = args

    def f(target: str, position: int = 0) -> ParseResult:
        messages = []
        for parser in parsers:
            parsed = parser.exec(target, position)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position)

    return Parser(f)


def seq(*args) -> Parser:
    r"""Seq function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> parse = seq(token('foo'), choice(token('bar'), token('baz')))
    >>> parse.exec('foobar')
    ['foo', 'bar']
    >>> parse.exec('foobaz')
    ['foo', 'baz']
    >>> parse.exec('foo')
    parse error at (3): unexpected  expecting bar
    parse error at (3): unexpected  expecting baz
    """  # noqa: E501
    parsers = args

    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos_org = position
        for parser in parsers:
            parsed = parser.exec(target, position)
            if not parsed.success:
                return Failure(parsed.message, pos_org)
            if parsed.tokens is None:
                continue
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            position = parsed.position

        return Success(result, position)

    return Parser(f)


def option(parser: Parser) -> Parser:
    """Option function.

    Example
    -------
    >>> from simpleparser.prim import token
    >>> parser = option(token('hoge'))
    >>> parser.exec('hoge', 0)
    ['hoge']
    >>> parser.exec('fuga', 0)
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if result.success:
            return result
        return Success([], position)

    return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
