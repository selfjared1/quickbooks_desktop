
import re

def camel_to_snake_dict(data):
    new_data = {}
    for k, v in data.items():
        new_k = camel_to_snake_str(k)
        new_data[new_k] = v
    return new_data

def camel_to_snake_str(name):
    """Convert camelCase keys in a dictionary to snake_case keys."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake_case

def snake_to_camel_str(name):
    """Convert snake_case keys in a dictionary to camelCase keys."""
    parts = name.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])