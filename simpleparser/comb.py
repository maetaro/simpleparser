"""a parser function's combinator."""
import inspect
from types import FrameType
from typing import List, Callable, cast, Any
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
    parse error at (0): unexpected bar expecting foo (by token)
    >>> p.exec('foobar')
    ['foo']
    """
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function

    def f(target: str, position: int = 0) -> ParseResult:
        result: List[str] = []
        pos: int = position
        first: bool = True
        children = []

        while True:
            parsed = parser.exec(target, pos)
            children.append(parsed)
            if not parsed.success:
                if first:
                    return Failure(parsed.message, position, children=children, name=name)
                break
            if parsed.position > len(target):
                break
            result.extend(parsed.tokens)
            first = False
            pos = parsed.position

        return Success(result, pos, children=children, name=name)

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
    parse error at (0): unexpected ali expecting foo (by token)
    parse error at (0): unexpected ali expecting bar (by token)
    """
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function
    parsers = args
    assert len(args) >= 2
    children = []

    def f(target: str, position: int = 0) -> ParseResult:
        messages = []
        for parser in parsers:
            parsed = parser.exec(target, position)
            children.append(parsed)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position, children=children, name=name)

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
    parse error at (3): unexpected  expecting bar (by token)
    >>> p.exec('foobaz')
    parse error at (3): unexpected baz expecting bar (by token)
    """
    assert len(args) >= 2
    parsers = args
    children = []
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function

    def f(target: str, position: int = 0) -> ParseResult:
        result: List[str] = []
        pos_org = position
        for parser in parsers:
            parsed: ParseResult = parser.exec(target, position)
            children.append(parsed)
            if not parsed.success:
                return Failure(parsed.message, pos_org, children=children, name=name)
            if parsed.tokens is None:
                continue
            result.extend(parsed.tokens)
            position = parsed.position

        return Success(result, position, children=children, name=name)

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
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function

    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        children = [result]
        if result.success:
            return result
        return Success([], position, children=children, name=name)

    return Parser(f)


def transform(parser: Parser, selector: Callable[[List[str]], Any]) -> Parser:  # noqa E501
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
    >>> p = transform(token("foo"), lambda x: [",".join(x) + " aaa"])
    >>> p.exec("foo")
    ['foo aaa']
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if not result.success:
            return result
        result.tokens = selector(result.tokens)
        return result

    return Parser(f)


def end_by(parser: Parser, sep: Parser) -> Parser:
    """Endby p sep parses zero or more occurrences of p, separated and ended by sep.

    Returns a list of values returned by p.

    Example
    -------
    >>> from simpleparser import token, end_by
    >>> p = end_by(token('foo'), token(','))
    >>> p.exec('foo,foo,')
    ['foo', 'foo']
    >>> p.exec('foo,foo')
    parse error at (0): unexpected foo,f expecting foo (by token)
    >>> p.exec('foo,foo,-')
    parse error at (0): unexpected foo,f expecting foo (by token)
    """  # noqa: D401, E501
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function

    def f(target: str, position: int = 0) -> ParseResult:
        tokens = []
        pos: int = position
        last_is_not_sep = False
        results = []
        children = []

        while pos < len(target):
            parsed = parser.exec(target, pos)
            children.append(parsed)
            results.append(parsed)
            if not parsed.success:
                msg = (f"parse error at ({position}):"
                       f" unexpected {target[position:position + 5]}"
                       f" expecting {parser.expression} (by {parser.parser_type})")
                return Failure(msg, pos, children=results, name=name)
                # break
            if parsed.success:
                last_is_not_sep = True
            tokens.extend(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            children.append(parsed)
            results.append(parsed)
            if not parsed.success:
                # fail
                msg = (f"parse error at ({position}):"
                       f" unexpected {target[position:position + 5]}"
                       f" expecting {parser.expression} (by {parser.parser_type})")
                return Failure(msg, pos, children=results, name=name)
                # break
            if parsed.success:
                last_is_not_sep = False
            pos = parsed.position

        if last_is_not_sep:
            msg = (f"parse error at ({position}):"
                   f" unexpected {target[position:position + 5]}"
                   f" expecting {parser.expression} (by {parser.parser_type})")
            return Failure(msg, pos, children=results, name=name)

        # if pos != len(target):
        #     msg = (f"parse error at ({position}):"
        #            f" unexpected {target[position:position + 5]}"
        #            f" expecting {parser.expression} (by {parser.parser_type})")
        #     return Failure(msg, pos)

        return Success(tokens, pos, children=results, name=name)

    return Parser(f)


def sep_by(parser: Parser, sep: Parser) -> Parser:
    """Parse zero or more occurrences of parser, separated by sep.

    Returns a list of values returned by parser.

    Example
    -------
    >>> from simpleparser import token, sep_by
    >>> p = sep_by(token('foo'), token(','))
    >>> p.exec('foo,foo')
    ['foo', 'foo']
    """
    name = inspect.getframeinfo(cast(FrameType, inspect.currentframe())).function

    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos = position
        children = []

        while True:
            parsed = parser.exec(target, pos)
            children.append(parsed)
            if not parsed.success:
                break
            result.extend(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            children.append(parsed)
            if not parsed.success:
                break
            pos = parsed.position

        return Success(result, pos, children=children, name=name)

    return Parser(f)


def lazy(callback: Callable[[], Parser]) -> Parser:
    """Lazy function.

    Example
    -------
    >>> from simpleparser import token, seq, option, lazy
    >>> p = option(seq(token('foo'), lazy(lambda: p)))
    >>> p.exec('foo')
    ['foo']
    >>> p.exec('foofoo')
    ['foo', 'foo']
    """
    def f(target: str, position: int) -> ParseResult:
        parse = callback()
        return parse.exec(target, position)

    return Parser(f)
