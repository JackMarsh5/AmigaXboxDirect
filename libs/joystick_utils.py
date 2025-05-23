# libs/joystick_utils.py

class Vec2:
    """Simple container for keeping joystick coords in x & y terms.

    Defaults to a centered joystick (0,0). Clips values to range [-1.0, 1.0], as with the Amiga joystick.
    """
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = min(max(-1.0, x), 1.0)
        self.y: float = min(max(-1.0, y), 1.0)

    def __str__(self) -> str:
        return f"({self.x:0.2f}, {self.y:0.2f})"

def scale_axis(value, center=128, span=128):
    """Convert 0–255 range to -1.0 to 1.0 for joystick axis."""
    return (value - center) / float(span)

def clip(value, min_value=-1.0, max_value=1.0):
    """Clamp a value between min and max."""
    return max(min_value, min(value, max_value))
