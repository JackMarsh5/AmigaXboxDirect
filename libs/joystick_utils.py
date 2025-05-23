# libs/joystick_utils.py

def scale_axis(value, center=128, span=128):
    """Convert 0–255 range to -1.0 to 1.0 for joystick axis."""
    return (value - center) / float(span)


def clip(value, min_value=-1.0, max_value=1.0):
    """Clamp a value between min and max."""
    return max(min_value, min(value, max_value))
