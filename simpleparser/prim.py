"""a simple parser combinator."""

# from mod1 import Parser, ParseResult, Success, Failure


# def token(s: str) -> Parser:
#     """Token function.

#     Example
#     -------
#     >>> token("foo").exec("foobar").result()
#     ['foo']
#     >>> token("bar").exec("foobar").result()
#     'parse error at (0): unexpected foo expecting bar'
#     """
#     length: int = len(s)

#     def f(target: str, position: int = 0) -> ParseResult:
#         if target[position:position + length] == s:
#             return Success([s], position + length)
#         msg = ("parse error at (" + str(position) + "):"
#                " unexpected " + target[position:position + length] + ""
#                " expecting " + s + "")
#         return Failure(msg, position)

#     return Parser(f)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
