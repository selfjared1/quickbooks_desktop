import json
from datetime import datetime


def to_lower_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # Capitalize the first letter of each component
    return ''.join(x.title() for x in components)


def convert_datetime(date_str):
    if isinstance(date_str, str):
        if date_str == '':
            return None
        else:
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError as e:
                raise ValueError(f"Invalid date format: {e}")
    elif isinstance(date_str, datetime):
        return date_str  # Already a datetime object, no conversion needed
    else:
        return None  # None or other inappropriate data types


def convert_float(float_str):
    if float_str == "":
        return None  # Return None immediately if the input is an empty string
    try:
        return float(float_str)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid input for float conversion: {e}")


def convert_to_json_string(data):
    if isinstance(data, (dict, list)):
        return json.dumps(data)
    return data


def convert_all_dicts_and_lists(obj):
    """
    Go through all attributes of an object, converting any that are dictionaries to JSON strings.
    """
    for key, value in vars(obj).items():
        setattr(obj, key, convert_to_json_string(value))


def convert_integer(value):
    if isinstance(value, int):
        if value == 1:
            return 'True'
        elif value == 0:
            return 'False'
        else:
            return str(value)
    return value
