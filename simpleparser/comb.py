"""a parser function's combinator."""

from typing import List, Callable
from simpleparser.parseresult import ParseResult, Success, Failure
from simpleparser.parser import Parser


def many(parser: Parser) -> Parser:
    """Many function.

    Receives one parser object.
    And repeats parsing for success.
    Must succeed at least once.

    Parameters
    ----------
    parser
        The Parser object.

    Returns
    -------
    Parser
        Generated new Parser object.

    Example
    -------
    >>> from simpleparser import many, token
    >>> p = many(token("foo"))
    >>> p.exec('foo')
    ['foo']
    >>> p.exec('foofoo')
    ['foo', 'foo']
    >>> p.exec('bar')
    parse error at (0): unexpected bar expecting foo
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result: List[str] = []
        pos: int = position
        first: bool = True

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                if first:
                    return Failure(parsed.message, position)
                break
            result.extend(parsed.tokens)
            first = False
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def choice(*args: Parser) -> Parser:
    """Choice function.

    Receive multiple parser objects.
    And even one succeeds, this parser is also treated as successful.

    Parameters
    ----------
    args
        The Parser objects.

    Returns
    -------
    Parser
        Generated new Parser object.

    Example
    -------
    >>> from simpleparser import token, choice
    >>> p = choice(token('foo'), token('bar'))
    >>> p.exec('foo')
    ['foo']
    >>> p.exec('bar')
    ['bar']
    >>> p.exec('alice')
    parse error at (0): unexpected ali expecting foo
    parse error at (0): unexpected ali expecting bar
    """
    parsers = args
    assert len(args) >= 2

    def f(target: str, position: int = 0) -> ParseResult:
        messages = []
        for parser in parsers:
            parsed = parser.exec(target, position)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position)

    return Parser(f)


def seq(*args: Parser) -> Parser:
    """Seq function.

    Receives multiple parser objects.
    Received parsers are executed in order.
    And all succeed, this parser will also be treated as successful.

    Parameters
    ----------
    args
        The Parser objects.

    Returns
    -------
    Parser
        Generated new Parser object.

    Example
    -------
    >>> from simpleparser import token, seq
    >>> p = seq(token('foo'), token('bar'))
    >>> p.exec('foobar')
    ['foo', 'bar']
    >>> p.exec('foo')
    parse error at (3): unexpected  expecting bar
    >>> p.exec('foobaz')
    parse error at (3): unexpected baz expecting bar
    """
    assert len(args) >= 2
    parsers = args

    def f(target: str, position: int = 0) -> ParseResult:
        result: List[str] = []
        pos_org = position
        for parser in parsers:
            parsed: ParseResult = parser.exec(target, position)
            if not parsed.success:
                return Failure(parsed.message, pos_org)
            if parsed.tokens is None:
                continue
            result.extend(parsed.tokens)
            position = parsed.position

        return Success(result, position)

    return Parser(f)


def option(parser: Parser) -> Parser:
    """Option function.

    Receives one parser object.
    Regardless of the success or failure of Perth,
    this parser will always succeed.

    Parameters
    ----------
    parser
        The Parser object.

    Returns
    -------
    Parser
        Generated new Parser object.

    Example
    -------
    >>> from simpleparser import token, option
    >>> p = option(token('foo'))
    >>> p.exec('foobar')
    ['foo']
    >>> p.exec('bar')  # not fail.
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if result.success:
            return result
        return Success([], position)

    return Parser(f)


def transform(parser: Parser, selector: Callable[[List[str]], List[str]]) -> Parser:  # noqa E501
    """Transform function.

    Receives a parser object and a function that transforms the parse results.
    Apply the received function to the parse result and return it.

    Parameters
    ----------
    parser
        The Parser object.
    selector
        The function that formats and returns the parse result.

    Returns
    -------
    Parser
        Generated new Parser object.

    Example
    -------
    >>> from simpleparser import token, transform
    >>> transform(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo")
    ['foo aaa']
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if not result.success:
            return result
        result.tokens = selector(result.tokens)
        return result

    return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
