
import re
from datetime import datetime


def from_lxml_elements(
        cls,
        elements,
        combine_with_child_list=None,
        datetime_fields_list=['TimeCreated', 'TimeModified'],
        sublist_list=['DataExtRet']
    ):
    my_class = cls()
    for element in elements:
        # print(element.tag)
        if element.tag in datetime_fields_list:
            date_object = datetime.strptime(element.text, '%Y-%m-%dT%H:%M:%S%z')
            my_class.__setattr__(element.tag, date_object)
        elif element.tag in combine_with_child_list:
            for i in range(len(element)):
                my_class.__setattr__(element.tag + element[i].tag, element[i].text)
        elif element.tag in sublist_list:
            list_of_sub_elements = []
            for sub_element in element:
                sub_element_dict = {}
                for i in range(len(sub_element)):
                    sub_element_dict[sub_element.tag + sub_element[i].tag] = sub_element[i].text
                list_of_sub_elements += [sub_element_dict]
            my_class.__setattr__(element.tag, list_of_sub_elements)
        else:
            my_class.__setattr__(element.tag, element.text)
    return my_class

def remove_query_from_string(string_to_remove_from):
    if string_to_remove_from[-5:] == 'Query':
        string_to_remove_from = string_to_remove_from.replace('Query', '')
    else:
        pass
    return string_to_remove_from

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