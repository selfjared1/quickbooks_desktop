import json
from datetime import datetime
import unicodedata
import html
import re
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

def clean_text(input_element):
    input_str = et.tostring(input_element, encoding='unicode', method='html')
    strings_to_remove = ['&lt;', '&gt;']
    pattern = re.compile('|'.join(re.escape(s) for s in strings_to_remove))

    # Remove all specified strings
    cleaned_str = re.sub(pattern, '', input_str)
    cleaned_str = html.unescape(cleaned_str)
    replacement_dict = {
        'ñ': 'n', 'Ñ': 'N', '&': 'and', '’': '', 'é': 'e', 'É': 'E', '®': '', '…': '...',
        '“': '"', '”': '"', '–': '-', '™': '', 'Ü': 'U', 'ü': 'u', '×': 'x',
        'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'Ç': 'C',
        'È': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I', 'Ð': 'D',
        'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ø': 'dia', 'Ù': 'U', 'Ú': 'U',
        'Û': 'U', 'Ý': 'Y', 'Þ': 'Th', 'ß': 'ss', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a',
        'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i',
        'í': 'i', 'î': 'i', 'ï': 'i', 'ð': 'd', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ö': 'o', 'ø': 'dia', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ý': 'y', 'þ': 'th', 'ÿ': 'y',
        'Œ': 'OE', 'œ': 'oe', 'Š': 'S', 'š': 's', 'Ÿ': 'Y', 'ƒ': 'f', 'ˆ': '^', '˜': '~',
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta',
        'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu',
        'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'ς': 'sigma', 'σ': 'sigma',
        'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
        'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon', 'Ζ': 'Zeta',
        'Η': 'Eta', 'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa', 'Λ': 'Lambda', 'Μ': 'Mu',
        'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron', 'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau',
        'Υ': 'Upsilon', 'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi', 'Ω': 'Omega', ' ': 'NBSP', 'µm': 'micron',
        '±': '+/-', '°': 'deg', '€': 'EUR', 'ƒ': 'f', '„': '"', '†': '+', '‡': '++', '‰': 'per_mille',
        '‹': '<', '›': '>', '¡': '!', '¢': 'cent', '£': 'GBP', '¤': 'currency', '¥': 'JPY',
        '¦': '|', '§': 'S', '¨': '', '©': '(c)', 'ª': 'a', '«': '<<', '»': '>>',
        '¯': '-', '²': '2', '³': '3', '´': "'", 'µ': 'micro', '¶': 'P', '·': '.', '¹': '1',
        'º': 'o', '¼': '1/4', '½': '1/2', '¾': '3/4', '¿': '?', '×': 'x', '÷': '/', 'Þ': 'TH', 'þ': 'th'
    }
    for key, value in replacement_dict.items():
        cleaned_str = cleaned_str.replace(key, value)


    # cleaned_str = ''.join(c for c in unicodedata.normalize('NFKD', cleaned_str) if not unicodedata.combining(c))
    # output_element = et.fromstring(cleaned_str)

    normalized_str = unicodedata.normalize('NFKD', cleaned_str)
    cleaned_str = ''.join(c for c in normalized_str if not unicodedata.combining(c))

    try:
        output_element = et.fromstring(cleaned_str)
    except et.XMLSyntaxError:
        output_element = et.HTML(cleaned_str)
    return output_element