"""a parser module."""

from typing import Callable
from simpleparser.parseresult import ParseResult


class Parser:
    """a parser class."""

    def __init__(self, f: Callable[[str, int], ParseResult]):
        """Initialize method."""
        self.__f = f
        return

    @property
    def exec(self) -> Callable[[str, int], ParseResult]:
        """Return the executable function object."""
        return self.__f

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
