"""a parser module."""

from typing import Callable, TypeVar
from inspect import stack
from simpleparser.parseresult import ParseResult


class Parser:
    """a parser class."""

    def __init__(self, f: Callable[[str, int], ParseResult]):
        """Initialize method."""
        self.__f = f
        self.parser_type = [x for x in stack() if x.function !=
                            "__init__"][0].function
        self.expression = ""

    def exec(self, s: str, i: int = 0) -> ParseResult:
        """Return the executable function object."""
        return self.__f(s, i)

    # def __add__(self, other):
    #     r"""Add method.

    #     Example
    #     -------
    #     >>> parse = token('foo') + (token('bar') | token('baz'))
    #     >>> parse.exec('foobar')
    #     ['foo', 'bar']
    #     >>> parse.exec('foobaz')
    #     ['foo', 'baz']
    #     >>> parse.exec('foo')
    #     parse error at (3): unexpected  expecting bar
    #     parse error at (3): unexpected  expecting baz
    #     """  # noqa: E501
    #     return seq(self, other)

    # def __or__(self, other):
    #     """Or Method.

    #     Example
    #     -------
    #     >>> foo = token("foo")
    #     >>> bar = token("bar")
    #     >>> p = foo | bar
    #     >>> p.exec("foo")
    #     ['foo']
    #     """
    #     return choice(self, other)

    # def map(self, selector):
    #     """Map method.

    #     Example
    #     -------
    #     >>> cell = choice(token("foo"), token("bar")).map(lambda x: ["".join(x) + "aaa"])  # noqa F501
    #     >>> cell.exec("foooo")
    #     ['fooaaa']
    #     >>> cell.exec("barrr")
    #     ['baraaa']
    #     >>> map(token("foo"), lambda x: [",".join(x) + " aaa"]).exec("foo", 0)  # noqa F501
    #     ['foo aaa']
    #     """  # noqa: E501
    #     def f(target, position=0):
    #         result = self.exec(target, position)
    #         if not result.success:
    #             return result
    #         result.tokens = selector(result.tokens)
    #         return result

    #     return Parser(f)


T = TypeVar('T', bound='PrimitiveParser')


class PrimitiveParser(Parser):
    """a parser class."""

    def __init__(
            self,
            f: Callable[[T, str, int], ParseResult],
            expression: str):
        """Initialize method."""
        # super().__init__(f)
        self.__f2 = f
        self.parser_type = [x for x in stack() if x.function !=
                            "__init__"][0].function
        self.expression = expression

    def exec(self: T, s: str, i: int = 0) -> ParseResult:
        """Return the executable function object."""
        return self.__f2(self, s, i)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
