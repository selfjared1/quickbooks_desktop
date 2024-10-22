from lxml import etree as et
from typing import Any, Optional, Union, get_args, get_origin, List
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from sqlalchemy import func
import logging
from src.quickbooks_desktop.conversions import qb_to_sql
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.utilities import to_lower_camel_case
from src.quickbooks_desktop.qb_query_common_fields import NameFilter, NameRangeFilter


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

    def to_xml(self) -> et.Element:
        root = et.Element(self.Meta.name)

        # Retrieve the custom field order if available, otherwise use natural order
        field_order = getattr(self, 'FIELD_ORDER', None)

        # Get all fields from the dataclass
        fields = self._get_sorted_fields(field_order)

        for field in fields:
            value = getattr(self, field.name)
            if value is not None:
                element = self._create_xml_element(root, field, value)
                if element is not None:
                    root.append(element)

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
            return self._handle_list_value(root, field, value)
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
            parent_element.append(child)
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

        # Check for text content in the main element if no child elements matched
        if element is not None and not len(element) and element.text is not None and len(element.text) and element.text.replace('\n', '').strip() != '' and len(cls.__dataclass_fields__):
            main_field = next(iter(cls.__dataclass_fields__.values()))
            init_args[main_field.name] = element.text
        else:
            pass

        instance = cls(**init_args)
        return instance


class CopyFromParentMixin:

    @classmethod
    def copy_from_parent(cls, parent):
        instance = cls()
        for attr, value in parent.__dict__.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        return instance


class PluralMixin:

    # class Meta:
    #     name = ''
    #     plural_of = ''
    #     plural_of_db_model = ''


    def __init__(self):
        self._items = []

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        return len(self._items)

    def add_item(self, item):
        self._items.append(item)

    @classmethod
    def get_all_from_qb(cls, qb, include_custom_fields=False):
        QueryRq = et.Element(f'{cls.Meta.name}QueryRq')
        if include_custom_fields:
            custom_query = et.SubElement(QueryRq, 'OwnerID')
            custom_query.text = '0' #zero is the ownerID for all custom fields (not private fields)
        QueryRs = qb.send_xml(QueryRq)
        plural_instance = cls()
        for Ret in QueryRs:
            obj = plural_instance.Meta.plural_of.from_xml(Ret)
            plural_instance._items.append(obj)
        return plural_instance

    def to_list(self):
        return self._items

    @classmethod
    def from_xml(cls, list_of_ret):
        """A Ret should be passed in but it's sometimes not."""
        if not isinstance(list_of_ret, list):
            logger.debug(f'from_xml expects a list. Ret must be an instance of lxml.etree._Element. Your Ret is type {type(list_of_ret)}')
            logger.debug(f'list_of_ret is {list_of_ret}')
            raise TypeError(f'Ret must be an instance of lxml.etree._Element. Your Ret is type {type(list_of_ret)}')
        elif not len(list_of_ret):
            plural_instance = cls()
            return plural_instance
        elif list_of_ret[0].tag[-3:] != 'Ret':
            raise ValueError(f"Invalid tag: {list_of_ret[0].tag}. Must end with 'Ret' (as in RETurn from Quickbooks).")
        else:
            plural_instance = cls()
            for instance_xml in list_of_ret:
                plural_of_class = cls.Meta.plural_of
                plural_of_instance = plural_of_class.from_xml(instance_xml)
                plural_instance._items.append(plural_of_instance)
            return plural_instance

    def to_db(self, session=None):
        logger.debug('Began to_db')
        sqlalchemy_instances = []
        for dataclass_instance in self._items:
            sqlalchemy_instance = qb_to_sql(dataclass_instance, self.Meta.plural_of_db_model)
            sqlalchemy_instances.append(sqlalchemy_instance)
        logger.debug('Created sqlalchemy_instances.')
        with session.no_autoflush:
            for instance in sqlalchemy_instances:
                existing_instance = session.query(self.Meta.plural_of_db_model).filter_by(list_id=instance.list_id).first()
                if existing_instance:
                    # Delete the existing entry
                    session.delete(existing_instance)
                    session.commit()
                else:
                    pass
                session.add(instance)
            # # Commit the changes
            session.commit()
        logger.debug('Finished to_db')


    @classmethod
    def __get_last_time_modified_from_db(cls, session):
        max_time_modified = session.query(func.max(cls.Meta.plural_of_db_model.time_modified)).scalar()
        qb_max_time_modified = QBDates(max_time_modified)
        return qb_max_time_modified

    @classmethod
    def __get_from_qb_since_last_time_modified(cls, qb_max_time_modified, qb):
        plural_instance = cls()
        query = plural_instance.Meta.plural_of.Query()
        query.from_modified_date = qb_max_time_modified
        query_xml = query.to_xml()
        QueryRs = qb.send_xml(query_xml)
        for Ret in QueryRs:
            obj = plural_instance.Meta.plural_of.from_xml(Ret)
            plural_instance._items.append(obj)
        return plural_instance

    @classmethod
    def update_db(cls, qb, session):
        qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
        plural_instance = cls.__get_from_qb_since_last_time_modified(qb_max_time_modified, qb)
        plural_instance.to_db(session)

    @classmethod
    def populate_db(cls, qb, session):
        instances = cls.get_all_from_qb(qb)
        instances.to_db(session)

    @classmethod
    def populate_or_update_db(cls, qb, session):
        qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
        if qb_max_time_modified:
            cls.update_db(qb, session)
        else:
            cls.populate_db(qb, session)


class PluralListSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for item in self:
            if item.list_id is not None:
                mod_xml = item._get_mod_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = item._get_add_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response



class QBQueryMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}QueryRq"

class QBAddMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CopyFromParentMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}AddRq"


class QBModMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CopyFromParentMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}ModRq"

class ListSaveMixin:

    def _get_mod_xml(self):
        mod_class = getattr(self, f'{self.Meta.name}mod', None)
        mod_instance = mod_class.copy_from_parent(self)
        mod_xml = mod_instance.to_xml()
        return mod_xml

    def _get_add_xml(self):
        add_class = getattr(self, f'{self.Meta.name}mod', None)
        add_instance = add_class.copy_from_parent(self)
        add_xml = add_instance.to_xml()

    def save(self, qb):
        if self.list_id is not None:
            mod_xml = self._get_mod_xml()
            response = qb.send_xml(mod_xml)
            return response
        else:
            add_xml = self._get_add_xml()
            response = qb.send_xml(add_xml)
            return response



class QBMixin(MaxLengthMixin, ToXmlMixin, FromXmlMixin, ValidationMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


class QBMixinWithQuery(QBMixin):

    # class Query(QBQueryMixin):
    #     pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Query.set_name(cls.Meta.name)


class DataExtTypeValue(Enum):
    AMTTYPE = "AMTTYPE"
    DATETIMETYPE = "DATETIMETYPE"
    INTTYPE = "INTTYPE"
    PERCENTTYPE = "PERCENTTYPE"
    PRICETYPE = "PRICETYPE"
    QUANTYPE = "QUANTYPE"
    STR1024_TYPE = "STR1024TYPE"
    STR255_TYPE = "STR255TYPE"

@dataclass
class DataExtType(QBMixin):

    class Meta:
        name = "DataExtType"

    _value: Optional[DataExtTypeValue] = field(default=None, init=False)

    @property
    def value(self) -> Optional[DataExtTypeValue]:
        return self._value

    @value.setter
    def value(self, new_value: Any):
        if new_value is not None and not isinstance(new_value, DataExtTypeValue):
            raise ValueError(f"Invalid value: {new_value}. Must be an instance of DataExtTypeValue.")
        self._value = new_value

@dataclass
class OwnerId(QBMixin):
    class Meta:
        name = "OwnerID"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"0|(\{[0-9a-fA-F]{8}(\-([0-9a-fA-F]{4})){3}\-[0-9a-fA-F]{12}\})",
        },
    )

@dataclass
class DataExtValue(QBMixin):
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )

@dataclass
class DataExtRet(QBMixin):
    owner_id: Optional[OwnerId] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
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
    data_ext_type: Optional[DataExtType] = field(
        default=None,
        metadata={
            "name": "DataExtType",
            "type": "Element",
            "required": True,
        },
    )
    data_ext_value: Optional[DataExtValue] = field(
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



