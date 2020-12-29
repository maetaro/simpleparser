"""a simple parser combinator."""

from typing import List, Callable, TypeVar


T = TypeVar('T', bound='ParseResult')


class ParseResult:
    """Parsed Result class."""

    def __init__(self, success: bool, tokens: List[str],
                 position: int, message: str = "") -> None:
        """Initialize method."""
        self.success: bool = success
        self.tokens: List[str] = tokens
        self.position: int = position
        self.message: str = message

    def then(self: T, f: Callable[[T], None]) -> T:
        """Execute function then parse is success."""
        if self.success:
            f(self)
        return self

    def catch(self: T, f: Callable[[T], None]) -> T:
        """Execute function then parse is success."""
        if not self.success:
            f(self)
        return self


class Success(ParseResult):
    """Parsed Success class."""

    def __init__(self, tokens: List[str], position: int) -> None:
        """Initialize method."""
        super().__init__(True, tokens, position)

    def __repr__(self) -> str:
        """Return string."""
        return str(self.tokens)


class Failure(ParseResult):
    """Parsed Failure class."""

    def __init__(self, message: str, position: int) -> None:
        """Initialize method."""
        super().__init__(False, [], position, message)

    def __repr__(self) -> str:
        """Return string."""
        return self.message


if __name__ == "__main__":
    import doctest
    doctest.testmod()
