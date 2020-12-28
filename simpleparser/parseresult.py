"""a simple parser combinator."""


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
