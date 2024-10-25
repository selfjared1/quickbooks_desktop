from lxml import etree as et
from typing import Any, Optional, Union, get_args, get_origin
from dataclasses import dataclass, field, fields, is_dataclass
import logging
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.utilities import to_lower_camel_case

logger = logging.getLogger(__name__)


yes_no_dict = {'Yes': True, 'yes': True, 'No': False, 'no': False}

class MaxLengthMixin:
    def __setattr__(self, key: str, value: Any) -> None:
        field_info = next((field for field in fields(self) if field.name == key), None)
        if field_info:
            max_length = field_info.metadata.get('max_length')
            if max_length and isinstance(value, str) and len(value) > max_length:
                raise ValueError(f"Value for {field_info.name} field '{key}' exceeds the maximum allowed length of {max_length}")
        super().__setattr__(key, value)


class ToXmlMixin:
    IS_YES_NO_FIELD_LIST = []

    def to_xml(self):
        root = et.Element(self.Meta.name)

        # Retrieve the custom field order if available, otherwise use natural order
        field_order = getattr(self, 'FIELD_ORDER', None)

        # Get all fields from the dataclass
        fields = self._get_sorted_fields(field_order)

        for field in fields:
            value = getattr(self, field.name)
            if value is not None and not isinstance(value, type):
                element = self._create_xml_element(root, field, value)
                if element is not None:
                    root.append(element)
                else:
                    pass
            else:
                pass

        return root

    def _get_sorted_fields(self, field_order):
        """
        Return the fields sorted by the given field order.
        If no field order is provided, return them in natural order.
        """
        fields = list(self.__dataclass_fields__.values())
        if field_order:
            fields.sort(key=lambda f: field_order.index(f.name) if f.name in field_order else len(field_order))
        return fields

    def _create_xml_element(self, root, field, value):
        """
        Create an XML element based on the field and value.
        """
        if isinstance(value, list):
            element = self._handle_list_value(root, field, value)
            return element
        elif isinstance(value, bool):
            return self._handle_bool_value(field, value)
        elif isinstance(value, QBDates) or isinstance(value, QBTime):
            return value.to_xml(field.name)
        elif is_dataclass(value):
            return value.to_xml()
        else:
            return self._handle_simple_value(field, value)

    def _handle_list_value(self, root, field, value_list):
        """
        Handle list values, creating XML elements for each item in the list.
        """
        if len(value_list) == 0:
            return None

        parent_element = et.Element(field.metadata.get("name", field.name))
        for child in value_list:
            if isinstance(child, et._Element):
                parent_element.append(child)
            else:
                element = child.to_xml()
                return element
        return parent_element

    def _handle_bool_value(self, field, value):
        """
        Handle boolean values, converting them to 'Yes/No' or 'true/false' based on IS_YES_NO_FIELD_LIST.
        """
        field_name = field.metadata.get("name", field.name)
        element = et.Element(field_name)
        if field_name in self.IS_YES_NO_FIELD_LIST:
            element.text = "Yes" if value else "No"
        else:
            element.text = "true" if value else "false"
        return element

    def _handle_simple_value(self, field, value):
        """
        Handle simple values, such as strings and numbers, converting them to text.
        """
        element = et.Element(field.metadata.get("name", field.name))
        element.text = str(value)
        return element



class ValidationMixin:
    validate_on_init: bool = True  # Default is to validate in __post_init__

    def __post_init__(self):
        if self.validate_on_init:
            self.validate()

    def validate(self) -> None:
        """
        Loop through all attributes in the class, check for 'valid_values' in metadata,
        and validate the attribute if valid values are present.
        """
        for field_name, field_def in self.__dataclass_fields__.items():
            valid_values = field_def.metadata.get("valid_values")
            attribute_value = getattr(self, field_name)

            # If valid_values exists, perform validation
            if valid_values is not None:
                # If the attribute is a list, validate each value
                if isinstance(attribute_value, list):
                    for single_value in attribute_value:
                        self._validate_str_from_list_of_values(field_name, single_value, valid_values)
                else:
                    # Single value validation
                    self._validate_str_from_list_of_values(field_name, attribute_value, valid_values)

    def _validate_str_from_list_of_values(self, attribute_name, qb_str, list_of_valid_values) -> None:
        if qb_str is not None and qb_str not in list_of_valid_values:
            raise ValueError(f"Invalid {attribute_name}: {qb_str}. Must be one of {list_of_valid_values}.")


class FromXmlMixin:

    #IS_YES_NO_FIELD_LIST shouldn't be populated until later down in inheritance so MRO shouldn't conflict
    IS_YES_NO_FIELD_LIST = []

    @staticmethod
    def __validate_from_xml_arg_type(element):
        if not isinstance(element, et._Element):
            raise TypeError(f'element must be an instance of lxml.etree._Element. Your element is type {type(element)}')
        # elif element.tag[-3:] != 'Ret':
        #     raise ValueError(f"Invalid tag: {element.tag}. Must end with 'Ret' (as in RETurn from Quickbooks).")
        else:
            pass

    @staticmethod
    def __get_field_type(field):
        field_type = field.type
        if get_origin(field_type) is Union:
            # Handle Optional and Union types
            field_type = next(arg for arg in get_args(field_type) if arg is not type(None))
            return field_type
        else:
            return field_type

    @staticmethod
    def __parse_list_field_type(init_args, field, field_type, xml_element):
        # if the field type is a list
        class_to_use = field_type.__args__[0]
        instance = class_to_use.from_xml(xml_element)
        if field.name in init_args.keys():
            init_args[field.name].append(instance)
        else:
            init_args[field.name] = [instance]
        return init_args


    @classmethod
    def __parse_field_according_to_type(cls, init_args, field, field_type, xml_element):
        # Check if the field type is a dataclass
        if is_dataclass(field_type):
            init_args[field.name] = field_type.from_xml(xml_element)
        elif hasattr(field_type, '_name') and field_type._name == 'List':
            init_args = cls.__parse_list_field_type(init_args, field, field_type, xml_element)
        elif field.name in cls.IS_YES_NO_FIELD_LIST:
            init_args[field.name] = yes_no_dict[xml_element.text]
        else:
            try:
                init_args[field.name] = field_type(xml_element.text)
            except Exception as e:
                print(e)
        return init_args

    @classmethod
    def __get_init_args(cls, element, field_names):
        init_args = {}
        for xml_element in element:
            field_name = xml_element.tag
            if field_name == 'DataExtRet':  # Check for DataExtRet tag
                ext_name = to_lower_camel_case(
                    xml_element.find('DataExtName').text.replace(' ', '_').lower())  # Convert to lower camel case
                ext_value = xml_element.find('DataExtValue').text
                init_args[ext_name] = ext_value
            elif field_name in field_names:
                field = field_names[field_name]
                field_type = cls.__get_field_type(field)
                init_args = cls.__parse_field_according_to_type(init_args, field, field_type, xml_element)
            else:
                logger.debug(f'Extra field {field_name} is in the xml provided')
        return init_args

    @classmethod
    def from_xml(cls, element: et.Element) -> Any:
        cls.__validate_from_xml_arg_type(element)

        field_names = {field.metadata.get("name", field.name): field for field in cls.__dataclass_fields__.values()}
        init_args = cls.__get_init_args(element, field_names)

        if element is not None:
            if not len(element) and element.text is not None and len(element.text) and element.text.replace('\n', '').strip() != '' and len(cls.__dataclass_fields__):
                main_field = next(iter(cls.__dataclass_fields__.values()))
                init_args[main_field.name] = element.text
            elif element.tag in ['InvoiceLineRet']:
                from src.quickbooks_desktop.transactions.invoices import InvoiceLine
                for line in element:
                    invoice_line = InvoiceLine.from_xml(line)
                    return invoice_line
            else:
                pass
        else:
            pass

        instance = cls(**{k: v for k, v in init_args.items() if k in cls.__dataclass_fields__})

        all_xml_fields = {child.tag: child.text for child in element}
        extra_fields = {k: v for k, v in all_xml_fields.items() if k not in field_names}

        for field_name, field_value in extra_fields.items():
            setattr(instance, field_name, field_value)

        return instance


class ReprMixin:
    def __repr__(self):
        # Collect all field values dynamically
        field_strings = []

        for field in self.__dataclass_fields__.values():
            value = getattr(self, field.name)
            # If the value is a list, show a summary
            if isinstance(value, list):
                field_strings.append(f"{field.name}=[...({len(value)} items)]")
            else:
                field_strings.append(f"{field.name}={repr(value)}")

        # Build the final repr string using the class name and its dynamic fields
        field_str = ", ".join(field_strings)
        return f"{self.__class__.__name__}({field_str})"

class CopyFromParentMixin:

    @classmethod
    def copy_from_parent(cls, parent):
        instance = cls()
        for attr, value in parent.__dict__.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            elif attr[-4:] == '_ret' and hasattr(instance, str(attr[:-4]) + '_add') and isinstance(value, list):
                converted_values = []
                for sub_instance in value:
                    add_class = getattr(sub_instance, 'Add')
                    add_value = add_class.copy_from_parent(sub_instance)
                    converted_values.append(add_value)
                setattr(instance, str(attr[:-4]) + '_add', converted_values)
            else:
                pass

        return instance


class QBQueryMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}QueryRq"

class QBAddMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CopyFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}AddRq"


class QBModMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CopyFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}ModRq"

class SaveMixin:

    def _get_mod_rq_xml(self):
        mod_class = getattr(self, f'Mod', None)
        mod_instance = mod_class.copy_from_parent(self)
        mod_xml = mod_instance.to_xml()
        rq_element_name = mod_class.__name__ + 'Rq'
        rq_element = et.Element(rq_element_name)
        rq_element.append(mod_xml)
        return rq_element

    def _get_add_rq_xml(self):
        add_class = getattr(self, f'Add', None)
        add_instance = add_class.copy_from_parent(self)
        add_xml = add_instance.to_xml()
        rq_element_name = add_class.__name__ + 'Rq'
        rq_element = et.Element(rq_element_name)
        rq_element.append(add_xml)
        return rq_element

    def save(self, qb):
        if self.list_id is not None:
            mod_xml = self._get_mod_rq_xml()
            response = qb.send_xml(mod_xml)
            return response
        else:
            add_xml = self._get_add_rq_xml()
            response = qb.send_xml(add_xml)
            return response



class QBMixin(MaxLengthMixin, ToXmlMixin, FromXmlMixin, ValidationMixin, ReprMixin, SaveMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


class QBMixinWithQuery(QBMixin):

    # class Query(QBQueryMixin):
    #     pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Query.set_name(cls.Meta.name)

@dataclass
class DataExtRet(QBMixin):
    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
            "pattern": r"0|(\{[0-9a-fA-F]{8}(\-([0-9a-fA-F]{4})){3}\-[0-9a-fA-F]{12}\})",
        },
    )
    data_ext_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtName",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "AMTTYPE", "DATETIMETYPE", "INTTYPE", "PERCENTTYPE",
                "PRICETYPE", "QUANTYPE", "STR1024TYPE", "STR255TYPE"
            ]
        },
    )
    data_ext_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtValue",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class QBRefMixin(QBMixin):

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 209
        },
    )



