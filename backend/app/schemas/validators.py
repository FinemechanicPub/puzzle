from pydantic_core.core_schema import FieldValidationInfo


def validate_color(value):
    if isinstance(value, str):
        return int(value, 16)
    if isinstance(value, int):
        return value
    raise ValueError("Value cannot be converted to integer number")
