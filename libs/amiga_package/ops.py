"""Template module with math functions."""

def add(a: int, b: int) -> int:
    """Template function to add two integer values."""
    assert isinstance(a, int), f"Argument 'a' is not an integer. Got: {type(a)}"
    assert type(a) == type(b), f"Type of 'b' must match type of 'a'. Got: {type(b)}"
    return a + b
