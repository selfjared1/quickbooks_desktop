import re
import os
import html
import json
import unicodedata
import pathlib
from datetime import datetime
from lxml import etree as et


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


def encode_special_characters(input_string):

    REPLACEMENT_DICT = {
        # XML predefined entities
        '&': '&amp;',
        '"': '&quot;',
        "'": '&apos;',

        # Common special characters encoded as numeric references
        'ñ': '&#241;', 'Ñ': '&#209;', '’': '&#8217;', 'é': '&#233;', 'É': '&#201;',
        '®': '&#174;', '…': '&#8230;', '“': '&#8220;', '”': '&#8221;', '–': '&#8211;',
        '™': '&#8482;', 'Ü': '&#220;', 'ü': '&#252;', '×': '&#215;',

        # Extended Latin characters
        'À': '&#192;', 'Á': '&#193;', 'Â': '&#194;', 'Ã': '&#195;', 'Ä': '&#196;',
        'Å': '&#197;', 'Æ': '&#198;', 'Ç': '&#199;', 'È': '&#200;', 'Ê': '&#202;',
        'Ë': '&#203;', 'Ì': '&#204;', 'Í': '&#205;', 'Î': '&#206;', 'Ï': '&#207;',
        'Ð': '&#208;', 'Ò': '&#210;', 'Ó': '&#211;', 'Ô': '&#212;', 'Õ': '&#213;',
        'Ö': '&#214;', 'Ø': '&#216;', 'Ù': '&#217;', 'Ú': '&#218;', 'Û': '&#219;',
        'Ý': '&#221;', 'Þ': '&#222;', 'ß': '&#223;', 'à': '&#224;', 'á': '&#225;',
        'â': '&#226;', 'ã': '&#227;', 'ä': '&#228;', 'å': '&#229;', 'æ': '&#230;',
        'ç': '&#231;', 'è': '&#232;', 'ê': '&#234;', 'ë': '&#235;', 'ì': '&#236;',
        'í': '&#237;', 'î': '&#238;', 'ï': '&#239;', 'ð': '&#240;', 'ò': '&#242;',
        'ó': '&#243;', 'ô': '&#244;', 'õ': '&#245;', 'ö': '&#246;', 'ø': '&#248;',
        'ù': '&#249;', 'ú': '&#250;', 'û': '&#251;', 'ý': '&#253;', 'þ': '&#254;',
        'ÿ': '&#255;',

        # Additional special characters
        'Œ': '&#338;', 'œ': '&#339;', 'Š': '&#352;', 'š': '&#353;', 'Ÿ': '&#376;',
        'ƒ': '&#402;', 'ˆ': '&#710;', '˜': '&#732;', 'α': '&#945;', 'β': '&#946;',
        'γ': '&#947;', 'δ': '&#948;', 'ε': '&#949;', 'ζ': '&#950;', 'η': '&#951;',
        'θ': '&#952;', 'ι': '&#953;', 'κ': '&#954;', 'λ': '&#955;', 'μ': '&#956;',
        'ν': '&#957;', 'ξ': '&#958;', 'ο': '&#959;', 'π': '&#960;', 'ρ': '&#961;',
        'ς': '&#962;', 'σ': '&#963;', 'τ': '&#964;', 'υ': '&#965;', 'φ': '&#966;',
        'χ': '&#967;', 'ψ': '&#968;', 'ω': '&#969;', 'Α': '&#913;', 'Β': '&#914;',
        'Γ': '&#915;', 'Δ': '&#916;', 'Ε': '&#917;', 'Ζ': '&#918;', 'Η': '&#919;',
        'Θ': '&#920;', 'Ι': '&#921;', 'Κ': '&#922;', 'Λ': '&#923;', 'Μ': '&#924;',
        'Ν': '&#925;', 'Ξ': '&#926;', 'Ο': '&#927;', 'Π': '&#928;', 'Ρ': '&#929;',
        'Σ': '&#931;', 'Τ': '&#932;', 'Υ': '&#933;', 'Φ': '&#934;', 'Χ': '&#935;',
        'Ψ': '&#936;', 'Ω': '&#937;', ' ': '&#160;', 'µm': '&#181;', '±': '&#177;',
        '°': '&#176;', '€': '&#8364;', '„': '&#8222;', '†': '&#8224;', '‡': '&#8225;',
        '‰': '&#8240;', '‹': '&#8249;', '›': '&#8250;', '¡': '&#161;', '¢': '&#162;',
        '£': '&#163;', '¤': '&#164;', '¥': '&#165;', '¦': '&#166;', '§': '&#167;',
        '¨': '&#168;', '©': '&#169;', 'ª': '&#170;', '«': '&#171;', '»': '&#187;',
        '¯': '&#175;', '²': '&#178;', '³': '&#179;', '´': '&#180;', 'µ': '&#181;',
        '¶': '&#182;', '·': '&#183;', '¹': '&#185;', 'º': '&#186;', '¼': '&#188;',
        '½': '&#189;', '¾': '&#190;', '¿': '&#191;', '÷': '&#247;', 'Þ': '&#222;',
        'þ': '&#254;',

        # Additional Currency Symbols
        '₹': '&#8377;', '₽': '&#8381;', '₩': '&#8361;',

        # Mathematical Symbols
        '∞': '&#8734;', '∆': '&#8710;',

        # Fractions
        '⅓': '&#8531;', '⅔': '&#8532;',

        # Arrows
        '→': '&#8594;', '←': '&#8592;',

        # Additional Punctuation
        '—': '&#8212;', '℗': '&#8471;', '℃': '&#8451;',
    }
    VALID_ENTITY_PATTERN = re.compile(r'&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);')

    def replacer(part):
        """
        Replace all characters using REPLACEMENT_DICT, except valid entities.
        """
        if VALID_ENTITY_PATTERN.fullmatch(part):
            return part  # Preserve valid entities
        return ''.join(REPLACEMENT_DICT.get(char, char) for char in part)

    # Split input string into parts based on valid entities
    parts = re.split(r'(&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);)', input_string)
    replaced_parts = [replacer(part) if not VALID_ENTITY_PATTERN.fullmatch(part) else part for part in parts]
    return_str = ''.join(replaced_parts)
    return return_str



def validate_qbxml(full_request, sdk_version):
    """
    Validate a QBXML string against the schema file for the given SDK version.

    Args:
        full_request (str): The QBXML content as a string.
        sdk_version (str): The QuickBooks SDK version (e.g., "13.0").

    Raises:
        ValueError: If the QBXML is invalid.
    """
    schema_filename = f"qbxml{sdk_version.replace('.', '')}.xsd"
    schema_path = os.path.join(os.path.dirname(__file__), "xsd_files", schema_filename)

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file for SDK version {sdk_version} not found at {schema_path}")

    with open(schema_path, "r", encoding="ISO-8859-1") as schema_file:
        schema_tree = et.parse(schema_file)

    schema = et.XMLSchema(schema_tree)

    try:
        doc = et.fromstring(full_request.encode("ISO-8859-1"))
        schema.assertValid(doc)
    except et.XMLSyntaxError as e:
        raise ValueError(f"Syntax Error in QBXML: {e}")
    except et.DocumentInvalid as e:
        raise ValueError(f"Validation Error in QBXML: {e}")



# def validate_special_characters(xml_string):
#     """
#     Validate special characters in the provided XML string.
#     Ensures no invalid characters are present based on XML's allowed Unicode range.
#     If invalid characters are found, locates and reports the problem.
#
#     Args:
#         xml_string (str): The XML content as a string.
#
#     Raises:
#         ValueError: If invalid characters are found, with the location in the XML.
#     """
#     # Define the regex pattern for valid XML characters
#     valid_char_pattern = re.compile(r"^[\u0009\u000A\u000D\u0020-\uD7FF\uE000-\uFFFD\u10000-\u10FFFF]*$")
#
#     # Quickly check the overall string for invalid characters
#     if not valid_char_pattern.match(xml_string):
#         # If invalid characters are detected, locate the issue
#         try:
#             # Parse the XML string into an element tree
#             root = et.fromstring(xml_string)
#         except et.XMLSyntaxError as e:
#             raise ValueError(f"XML parsing failed: {e}")
#
#         # Helper to validate text or tail for invalid characters
#         def has_invalid_characters(text):
#             return text and not valid_char_pattern.match(text)
#
#         # Recursively check elements to locate invalid characters
#         def find_invalid_element(element, path=""):
#             current_path = f"{path}/{element.tag}"
#
#             # Check element text
#             if has_invalid_characters(element.text):
#                 raise ValueError(
#                     f"Invalid characters in text of element '{current_path}': {repr(element.text)}"
#                 )
#
#             # Check element tail
#             if has_invalid_characters(element.tail):
#                 raise ValueError(
#                     f"Invalid characters in tail of element '{current_path}': {repr(element.tail)}"
#                 )
#
#             # Recursively check child elements
#             for child in element:
#                 find_invalid_element(child, current_path)
#
#         # Start detailed validation from the root element
#         find_invalid_element(root)
#     else:
#         pass
#
#     # Escape the entire XML string for QuickBooks SDK compatibility
#     escaped_string = html.escape(xml_string, quote=True)
#
#     return escaped_string