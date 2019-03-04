# -*- coding: utf-8 -*-

import re


class Maybe:
    def __init__(self, a):
        self.value = a
        return

    def bind(self, a_to_m_b):
        if self is Nothing:
            return Nothing
        else:
            return a_to_m_b(self.value)

    def __or__(self, a_to_m_b):
        return self.bind(a_to_m_b)


class Just(Maybe):
    def __repr__(self):
        return 'Just(%r)' % self.value


class Nothing(Maybe):
    def __repr__(self):
        return 'Nothing'
Nothing = Nothing(Nothing)


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


def token(s):
    """
    Example
    -------
    >>> token("foo")("foobar").result()
    ['foo']
    >>> token("bar")("foobar").result()
    'parse error at (0): unexpected foo expecting bar'
    """
    length = len(s)

    def f(target, position=0):
        if target[position:position + length] == s:
            return Success([s], position + length)
        else:
            return Failure("parse error at (" + str(position) + "): unexpected " + target[position:position + length] + " expecting " + s, position)

    return f


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
    >>> parser('hoge', 0).result()
    ['hoge']
    >>> parser = regex("([1-9][0-9]*)")
    >>> parser('2014a', 0).result()
    ['2014']
    >>> parser('01', 0).result()
    'parse error at (0): unexpected 01 expecting ([1-9][0-9]*)'
    """
    def f(target, position):
        m = re.match(pattern, target[position:])
        if m:
            return Success([m.group()], position + len(m.group()))
        else:
            return Failure("parse error at (" + str(position) + "): unexpected " + target[position:] + " expecting " + pattern, position)

    return f


def noneOf(s):
    """
    As the dual of oneOf, noneOf cs succeeds if the current character not in the supplied list of characters cs. Returns the parsed character.

    Example
    -------
    >>> noneOf("abcdefg")("hello", 0).result()
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
        else:
            return Failure("parse error at (" + str(position) + "): unexpected " + targetChar + " expecting " + s, position)

    return f


def char(s):
    """
    """
    return token(s)


def sepBy(parser, sep):
    """sepBy p sep parses zero or more occurrences of p, separated by sep. Returns a list of values returned by p.
    Example
    -------
    >>> sepBy(regex('\w*'), token(','))('hoge,hoge').result()
    ['hoge', ',', 'hoge']
    """
    def f(target, position=0):
        result = []
        pos = position

        while True:
            parsed = parser(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

            parsed = sep(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

        return Success(result, pos)

    return f


def many(parser):
    """
    Example
    -------
    >>> many(token('hoge'))('hogehoge').result()
    ['hoge', 'hoge']
    >>> many(token('hoge'))('', 0).result()
    []
    >>> many(token('foobar'))('foo', 0).result()
    []
    """
    def f(target, position=0):
        result = []
        pos = position

        while True:
            parsed = parser(target, pos)
            if not parsed.success:
                break
            if type(parsed.tokens) is list:
                result.extend(parsed.tokens)
            else:
                result.append(parsed.tokens)
            pos = parsed.position

        return Success(result, pos)

    return f


def choice(*args):
    """
    Example
    -------
    >>> parse = many(choice(token('hoge'), token('fuga')))
    >>> parse('', 0).result()
    []
    >>> parse('hogehoge', 0).result()
    ['hoge', 'hoge']
    >>> parse('fugahoge', 0).result()
    ['fuga', 'hoge']
    >>> parse('fugafoo', 0).result()
    ['fuga']
    """
    parsers = args

    def f(target, position):
        messages = []
        for parser in parsers:
            parsed = parser(target, position)
            if parsed.success:
                return parsed
            messages.append(parsed.message)

        return Failure("\n".join(messages), position)

    return f


def seq(*args):
    """
    Example
    -------
    >>> parse = seq(token('foo'), choice(token('bar'), token('baz')))
    >>> parse('foobar').result()
    ['foo', 'bar']
    >>> parse('foobaz').result()
    ['foo', 'baz']
    >>> parse('foo').result()
    'parse error at (3): unexpected  expecting bar\\nparse error at (3): unexpected  expecting baz'
    """
    parsers = args

    def f(target, position=0):
        result = []
        pos_org = position
        for parser in parsers:
            parsed = parser(target, position)
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

    return f


def option(parser):
    """
    Example
    -------
    >>> parser = option(token('hoge'))
    >>> parser('hoge', 0).result()
    ['hoge']
    >>> parser('fuga', 0).result()
    []
    """
    def f(target, position):
        result = parser(target, position)
        if result.success:
            return result
        else:
            return Success([], position)

    return f


def lazy(callback):
    """
    Example
    -------
    >>> parse = option(seq(token('hoge'), lazy(lambda: parse)))
    >>> parse('hoge', 0).result()
    ['hoge']
    >>> parse('hogehoge', 0).result()
    ['hoge', 'hoge']
    >>> parse('hogehogehoge', 0).result()
    ['hoge', 'hoge', 'hoge']
    """
    def f(target, position):
        parse = callback()
        return parse(target, position)
    return f


def map(parser, selector):
    """
    Example
    -------
    >>> map(token("foo"), lambda x: [",".join(x) + " aaa"])("foo", 0).result()
    ['foo aaa']
    """
    def f(target, position):
        result = parser(target, position)
        if not result.success:
            return result
        result.tokens = selector(result.tokens)
        return result

    return f


if __name__ == "__main__":
    import doctest
    doctest.testmod()
