def validate_color(value):
    if isinstance(value, str):
        return int(value, 16)
    if isinstance(value, int):
        return value
    raise ValueError("Value cannot be converted to integer number")
