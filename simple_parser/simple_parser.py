"""a simple parser combinator."""

import re


class ParseResult:
    """Parsed Result class."""

    def __init__(self, success: bool, tokens,
                 position: int, message: str = "") -> None:
        """Initialize method."""
        self.success: bool = success
        self.tokens = tokens
        self.position = position
        self.message: str = message

    def result(self):
        """Return parsed result."""
        # TODO: success()メソッドとcatch()メソッドにする。
        #       p.exec().success(lamdba result: print(result))など
        return [self.success, self.tokens, self.position]


class Success(ParseResult):
    """Parsed Success class."""

    def __init__(self, tokens, position: int):
        """Initialize method."""
        super().__init__(True, tokens, position)

    def result(self):
        """Return parsed result."""
        return self.tokens


class Failure(ParseResult):
    """Parsed Success class."""

    def __init__(self, message: str, position: int):
        """Initialize method."""
        super().__init__(False, None, position, message)

    def result(self):
        """Return parsed result."""
        return self.message


class Parser:
    """a parser class."""

    def __init__(self, f):
        """Initialize method."""
        self.__f = f
        return

    @property
    def exec(self):
        """Return the executable function object."""
        return self.__f

    def __add__(self, other):
        r"""Add method.

        Example
        -------
        >>> parse = token('foo') + (token('bar') | token('baz'))
        >>> parse.exec('foobar').result()
        ['foo', 'bar']
        >>> parse.exec('foobaz').result()
        ['foo', 'baz']
        >>> parse.exec('foo').result()
        'parse error at (3): unexpected  expecting bar\nparse error at (3): unexpected  expecting baz'
        """  # noqa: E501
        return seq(self, other)

    def __or__(self, other):
        """Or Method.

        Example
        -------
        >>> foo = token("foo")
        >>> bar = token("bar")
        >>> p = foo | bar
        >>> p.exec("foo").result()
        ['foo']
        """
        return choice(self, other)

    def map(self, selector):
        """Map method.

        Example
        -------
        >>> cell = (token("foo") | token("bar")).map(lambda x: ["".join(x) + "aaa"])
        >>> cell.exec("foooo").result()
        ['fooaaa']
        >>> cell.exec("barrr").result()
        ['baraaa']
        >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0).result()
        ['foo aaa']
        """  # noqa: E501
        def f(target, position=0):
            result = self.exec(target, position)
            if not result.success:
                return result
            result.tokens = selector(result.tokens)
            return result

        return Parser(f)


def token(s: str) -> Parser:
    """Token function.

    Example
    -------
    >>> token("foo").exec("foobar").result()
    ['foo']
    >>> token("bar").exec("foobar").result()
    'parse error at (0): unexpected foo expecting bar'
    """
    length = len(s)

    def f(target: str, position: int = 0) -> ParseResult:
        if target[position:position + length] == s:
            return Success([s], position + length)
        msg = ("parse error at (" + str(position) + "):"
               " unexpected " + target[position:position + length] + ""
               " expecting " + s + "")
        return Failure(msg, position)

    return Parser(f)


def regex(pattern: str) -> Parser:
    """Regex function returns a function that parses the beginning of the received string with the regular expression pattern.

    Parameters
    ----------
    pattern: str
        a regular expression string.
    Example
    -------
    >>> parser = regex("hoge")
    >>> parser.exec('hoge', 0).result()
    ['hoge']
    >>> parser = regex("([1-9][0-9]*)")
    >>> parser.exec('2014a', 0).result()
    ['2014']
    >>> parser.exec('01', 0).result()
    'parse error at (0): unexpected 01 expecting ([1-9][0-9]*)'
    """  # noqa: E501
    def f(target: str, position: int = 0) -> ParseResult:
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()))
        msg = ("parse error at (" + str(position) + "):"
               " unexpected " + target[position:] + ""
               " expecting " + pattern + "")
        return Failure(msg, position)

    return Parser(f)


def noneOf(s: str) -> Parser:
    """
    As the dual of oneOf, noneOf cs succeeds if the current character not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
    >>> noneOf("abcdefg").exec("hello", 0).result()
    ['h']
    """  # noqa: E501
    def f(target: str, position: int = 0):
        exists: bool = False
        targetChar: str = target[position:position + 1]
        for c in s:
            if targetChar == c:
                exists = True
                break
        if not exists:
            return Success([targetChar], position + 1)
        return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)  # noqa: E501

    return Parser(f)


def char(s: str) -> Parser:
    """Char function."""
    return token(s)


def endBy(parser: Parser, sep: Parser) -> Parser:
    r"""The endBy p sep parses zero or more occurrences of p, separated and ended by sep.

    Returns a list of values returned by p.

    Example
    -------
    >>> endBy(regex('\w*'), token(',')).exec('').result()
    ['']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge').result()
    ['hoge', 'hoge']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge,').result()
    ['hoge', 'hoge', '']
    >>> endBy(regex('\w*'), token(',')).exec('hoge,hoge,-').result()
    'parse error.'
    """  # noqa: D401, E501
    def f(target: str, position: int = 0) -> ParseResult:
        result = []
        pos: int = position

        while True:
            parsed = parser.exec(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

            parsed = sep.exec(target, pos)
            if not parsed.success:
                break
            pos = parsed.position

        if pos != len(target):
            return Failure("parse error.", pos)

        return Success(result, pos)

    return Parser(f)


def sepBy(parser: Parser, sep: Parser) -> Parser:
    r"""Parses zero or more occurrences of parser, separated by sep. Returns a list of values returned by parser.

    Example
    -------
    >>> sepBy(regex('\w*'), token(',')).exec('hoge,hoge').result()
    ['hoge', 'hoge']
    """  # noqa: D401, E501
    def f(target: str, position: int = 0):
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

            parsed = sep.exec(target, pos)
            if not parsed.success:
                break
            pos = parsed.position

        return Success(result, pos)

    return Parser(f)


def many(parser: Parser) -> Parser:
    """Many function.

    Example
    -------
    >>> many(token('hoge')).exec('hogehoge').result()
    ['hoge', 'hoge']
    >>> many(token('hoge')).exec('', 0).result()
    []
    >>> many(token('foobar')).exec('foo', 0).result()
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
    >>> parse = many(choice(token('hoge'), token('fuga')))
    >>> parse.exec('', 0).result()
    []
    >>> parse.exec('hogehoge', 0).result()
    ['hoge', 'hoge']
    >>> parse.exec('fugahoge', 0).result()
    ['fuga', 'hoge']
    >>> parse.exec('fugafoo', 0).result()
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


def seq(*args):
    r"""Seq function.

    Example
    -------
    >>> parse = seq(token('foo'), choice(token('bar'), token('baz')))
    >>> parse.exec('foobar').result()
    ['foo', 'bar']
    >>> parse.exec('foobaz').result()
    ['foo', 'baz']
    >>> parse.exec('foo').result()
    'parse error at (3): unexpected  expecting bar\nparse error at (3): unexpected  expecting baz'
    """  # noqa: E501
    parsers = args

    def f(target, position=0):
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


def option(parser: Parser):
    """Option function.

    Example
    -------
    >>> parser = option(token('hoge'))
    >>> parser.exec('hoge', 0).result()
    ['hoge']
    >>> parser.exec('fuga', 0).result()
    []
    """
    def f(target: str, position: int = 0) -> ParseResult:
        result = parser.exec(target, position)
        if result.success:
            return result
        return Success([], position)

    return Parser(f)


def lazy(callback) -> Parser:
    """Lazy function.

    Example
    -------
    >>> parse = option(seq(token('hoge'), lazy(lambda: parse)))
    >>> parse.exec('hoge', 0).result()
    ['hoge']
    >>> parse.exec('hogehoge', 0).result()
    ['hoge', 'hoge']
    >>> parse.exec('hogehogehoge', 0).result()
    ['hoge', 'hoge', 'hoge']
    """
    def f(target, position):
        parse = callback()
        return parse.exec(target, position)

    return Parser(f)


def map(parser: Parser, selector) -> Parser:
    """Map function.

    Example
    -------
    >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0).result()
    ['foo aaa']
    """  # noqa: E501
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
