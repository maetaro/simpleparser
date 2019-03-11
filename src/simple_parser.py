# -*- coding: utf-8 -*-

import re


class ParseResult:
    """Parsed Result class"""

    def __init__(self, success, tokens, position, message=""):
        self.success = success
        self.tokens = tokens
        self.position = position
        self.message = message

    def result(self):
        return [self.success, self.tokens, self.position]


class Success(ParseResult):

    def __init__(self, tokens, position):
        super().__init__(True, tokens, position)

    def result(self):
        return self.tokens


class Failure(ParseResult):

    def __init__(self, message, position):
        super().__init__(False, None, position, message)

    def result(self):
        return self.message


class Parser:
    """a parser class.
    """
    def __init__(self, f):
        self.__f = f
        return

    def bind(self, f):
        return f(self.f)

    @property
    def exec(self):
        return self.__f

    def __add__(self, other):
        return seq(self, other)

    def __or__(self, other):
        """
        >>> foo = token("foo")
        >>> bar = token("bar")
        >>> p = foo | bar
        >>> p.exec("foo").result()
        ['foo']
        """
        return choice(self, other)

    def map(self, selector):
        """
        Example
        -------
        >>> cell = (token("foo") | token("bar")).map(lambda x: ["".join(x) + "aaa"])
        >>> cell.exec("foooo").result()
        ['fooaaa']
        >>> cell.exec("barrr").result()
        ['baraaa']
        >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0).result()
        ['foo aaa']
        """
        def f(target, position=0):
            result = self.exec(target, position)
            if not result.success:
                return result
            result.tokens = selector(result.tokens)
            return result

        return Parser(f)


def token(s):
    """
    Example
    -------
    >>> token("foo").exec("foobar").result()
    ['foo']
    >>> token("bar").exec("foobar").result()
    'parse error at (0): unexpected foo expecting bar'
    """
    length = len(s)

    def f(target, position=0):
        if target[position:position + length] == s:
            return Success([s], position + length)
        return Failure("parse error at (" + str(position) + "): unexpected " + target[position:position + length] + " expecting " + s, position)

    return Parser(f)


def regex(pattern):
    """
    regex function returns a function that parses the beginning of the received string with the regular expression pattern.
    
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
    """
    def f(target, position):
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()))
        return Failure("parse error at (" + str(position) + "): unexpected " + target[position:] + " expecting " + pattern, position)

    return Parser(f)


def noneOf(s):
    """
    As the dual of oneOf, noneOf cs succeeds if the current character not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
    >>> noneOf("abcdefg").exec("hello", 0).result()
    ['h']
    """
    def f(target, position=0):
        exists = False
        targetChar = target[position:position + 1]
        for c in s:
            if targetChar == c:
                exists = True
                break
        if not exists:
            return Success([targetChar], position + 1)
        return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)

    return Parser(f)


def char(s):
    """
    """
    return token(s)


def endBy(parser, sep):
    """endBy p sep parses zero or more occurrences of p, separated and ended by sep. Returns a list of values returned by p.
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
    """
    def f(target, position=0):
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

        if pos != len(target):
            return Failure("parse error.", pos)

        return Success(result, pos)

    return Parser(f)


def sepBy(parser, sep):
    """sepBy(parser, sep) parses zero or more occurrences of parser, separated by sep. Returns a list of values returned by parser.
    Example
    -------
    >>> sepBy(regex('\w*'), token(',')).exec('hoge,hoge').result()
    ['hoge', 'hoge']
    """
    def f(target, position=0):
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


def many(parser):
    """
    Example
    -------
    >>> many(token('hoge')).exec('hogehoge').result()
    ['hoge', 'hoge']
    >>> many(token('hoge')).exec('', 0).result()
    []
    >>> many(token('foobar')).exec('foo', 0).result()
    []
    """
    def f(target, position=0):
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


def choice(*args):
    """
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

    def f(target, position=0):
        messages = []
        for parser in parsers:
            parsed = parser.exec(target, position)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position)

    return Parser(f)


def seq(*args):
    """
    Example
    -------
    >>> parse = seq(token('foo'), choice(token('bar'), token('baz')))
    >>> parse.exec('foobar').result()
    ['foo', 'bar']
    >>> parse.exec('foobaz').result()
    ['foo', 'baz']
    >>> parse.exec('foo').result()
    'parse error at (3): unexpected  expecting bar\\nparse error at (3): unexpected  expecting baz'
    """
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


def option(parser):
    """
    Example
    -------
    >>> parser = option(token('hoge'))
    >>> parser.exec('hoge', 0).result()
    ['hoge']
    >>> parser.exec('fuga', 0).result()
    []
    """
    def f(target, position):
        result = parser.exec(target, position)
        if result.success:
            return result
        return Success([], position)

    return Parser(f)


def lazy(callback):
    """
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


def map(parser, selector):
    """
    Example
    -------
    >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0).result()
    ['foo aaa']
    """
    def f(target, position):
        result = parser.exec(target, position)
        if not result.success:
            return result
        result.tokens = selector(result.tokens)
        return result

    return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
