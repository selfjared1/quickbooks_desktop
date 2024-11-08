import win32com.client, threading, time, logging, easygui
import xml.etree.ElementTree as ETree
from lxml import etree as et
from dataclasses import field
from collections import defaultdict

from .qb_special_fields import *
from .utilities import to_lower_camel_case

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())



# region Connection To Desktop And Utilities


@dataclass
class ErrorRecovery:
    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class QueryRs:
    class Meta:
        name = "QueryRs"

    ret: Optional[TempVar] = field(
        default=None,
        metadata={
            "name": "Ret",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    status_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "statusCode",
            "type": "Attribute",
            "required": True,
        },
    )
    status_severity: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusSeverity",
            "type": "Attribute",
            "required": True,
        },
    )
    status_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusMessage",
            "type": "Attribute",
        },
    )
    ret_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "retCount",
            "type": "Attribute",
        },
    )
    iterator_remaining_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "iteratorRemainingCount",
            "type": "Attribute",
        },
    )
    iterator_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "iteratorID",
            "type": "Attribute",
        },
    )

    @classmethod
    def from_xml(cls, xml_rs):
        pass

@dataclass
class QBRequest:
    data: Optional[TempVar] = field(
        default=None,
        metadata={
            "name": "Ret",
            "type": "Element",
        },
    )
    # include_ret_element: List[str] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "IncludeRetElement",
    #         "type": "Element",
    #         "max_length": 50,
    #     },
    # )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    response: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )


@dataclass
class QBRequests:

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
    def from_list(cls, items):
        instance = cls()
        for item in items:
            instance.add_item(item)
        return instance


class QuickbooksDesktop():
    """
    You'll need to run this in 32 Bit Python to work.
    QuickBooks Desktop session manager for XML.
    QuickBooks needs to be open and a company file open for this to work.
    The first time connecting you'll need to authorize the app inside of QuickBooks's UI.
    """

    def __init__(self, application_name="accountingpy", company_file=None, SDK_version='13.0'):
        self.application_name = application_name
        self.company_file = company_file
        self.session_begun = False
        self.keep_session_open = False
        self.connection_open = False
        self.keep_connection_open = False
        self.dispatch_str = "QBXMLRP2.RequestProcessor"
        self.qbXMLRP = None
        self.ticket = None
        self.SDK_version = SDK_version
        self.on_error="stopOnError" #options are continueOnError, rollbackOnError, stopOnError


    def dispatch(self):
        """
        This will create a Win32com object for QuickBooks Desktop then set qbXMLRP.

        """
        if self.qbXMLRP is None:
            if self.company_file is None:
                self.qbXMLRP = win32com.client.Dispatch(self.dispatch_str)
            else:
                print("company file isn't an option right now")
                #todo: make a way to connect to a specific file location

    def open_connection(self):
        """
        This will open a connection to QuickBooks Desktop.
        Note: This should ALWAYS be closed before closing the program.  Leaving the session open will make it to
            where QuickBooks Desktop cannot be closed.
        :param application_name: This is the name as it shows up in.
            QuickBooks>Edit>Preferences>Integrated Applications>Company Settings
        :return: None
        """

        try:
            self.dispatch()
            self.qbXMLRP.OpenConnection2('', self.application_name, 1)
            self.connection_open = True
        except Exception as e:
            raise Exception(f"There is an issue with Connecting to QuickBooks.  Here is the issue directly from QuickBooks: \n {e}")


    def begin_session(self):
        """
        This begins a session with QuickBooks Desktop.
        Note: This should ALWAYS be ended before closing the program.  Leaving the session open will make it to
            where QuickBooks Desktop cannot be closed.
        """
        try:
            if self.connection_open:
                self.ticket = self.qbXMLRP.BeginSession("", 0)
                self.session_begun = True
            else:
                self.open_connection()
                self.ticket = self.qbXMLRP.BeginSession("", 0)
                self.session_begun = True
        except:
            try:
                self.ticket = self.qbXMLRP.BeginSession("", 1)
                self.session_begun = True
            except Exception as e:
                print(e)

    def open_qb(self, application_name='accountingpy'):
        """
        The purpose of this is to combine open_connection and begin_session into a single command.
        """

        self.open_connection(application_name)
        self.begin_session()

    def _convert_to_lxml(self, requestXML):
        """
        Converts requestXML into an lxml.etree.Element, regardless of whether it is a string,
        xml.etree.ElementTree.Element, lxml.etree.Element, or a list of these types.

        :param requestXML: Can be a string, xml.etree.ElementTree.Element, lxml.etree.Element, or a list.
        :return: A single lxml.etree.Element or a list of lxml.etree.Element.
        """
        if isinstance(requestXML, list):
            # If it's a list, convert each item to lxml recursively
            converted_requests = []
            for item in requestXML:
                request_xml = self._convert_to_lxml(item)
                converted_requests.append(request_xml)
            return converted_requests

        if isinstance(requestXML, str):
            # If it's a string, parse it as XML
            try:
                requestXML = et.fromstring(requestXML)
                logger.debug("Converted string to lxml Element.")
                return requestXML
            except et.XMLSyntaxError as e:
                raise ValueError(f"Invalid XML string provided: {e}")


        elif isinstance(requestXML, ETree.Element):
            # If it's an xml.etree.ElementTree.Element, convert it to an lxml Element
            requestXML = et.fromstring(ETree.tostring(requestXML))
            logger.debug("Converted xml.etree.Element to lxml Element.")
            return requestXML


        elif isinstance(requestXML, et._ElementTree):
            # If it's an lxml ElementTree, return the root element
            logger.debug("requestXML is an lxml ElementTree. Converting to root element.")
            return requestXML.getroot()


        elif isinstance(requestXML, et._Element):
            # It's already an lxml element, no conversion needed
            logger.debug("requestXML is already an lxml Element.")
            return requestXML

        else:
            raise TypeError(f"requestXML is {type(requestXML)} type but it must be either a string, xml.etree.ElementTree.Element, lxml.etree.Element, or a list of these types")



    def _ensure_qbxml_structure(self, requestXML):
        """
        Ensures that the root element is QBXML, and QBXMLMsgsRq is a child of QBXML.

        :param requestXML: An lxml.etree.Element or list of elements representing the request(s).
        :return: A properly structured lxml.etree.Element with QBXML as the root and QBXMLMsgsRq inside.
        """
        # Initialize the root structure
        if isinstance(requestXML, list):
            QBXML = et.Element('QBXML')
            QBXMLMsgsRq = et.SubElement(QBXML, 'QBXMLMsgsRq', onError=self.on_error)
        elif requestXML.tag == 'QBXML':
            QBXML = requestXML
            QBXMLMsgsRq = QBXML.find('QBXMLMsgsRq')
        elif requestXML.tag == 'QBXMLMsgsRq':
            QBXML = et.Element('QBXML')
            QBXML.append(requestXML)
            QBXMLMsgsRq = requestXML
        else:
            # Neither QBXML nor QBXMLMsgsRq is the root, create new structure
            QBXML = et.Element('QBXML')
            QBXMLMsgsRq = et.SubElement(QBXML, 'QBXMLMsgsRq', onError=self.on_error)

        return QBXML, QBXMLMsgsRq

    def _get_class_name_from_response_tag(self, response_tag):
        if 'QueryRs' in response_tag:
            class_name = response_tag.replace('QueryRs', '')
        elif 'AddRs' in response_tag:
            class_name = response_tag.replace('AddRs', '')
        elif 'ModRs' in response_tag:
            class_name = response_tag.replace('ModRs', '')
        else:
            class_name = None
        return class_name

    def _create_response_list_from_elements(self):
        pass

    def _create_response_dict_from_responses(self, responses):
        instances = {}
        for response in responses:
            request_id = response.get("requestID")
            status_code = response.get("statusCode")
            status_severity = response.get("statusSeverity")
            status_message = response.get("statusMessage")
            class_name = self._get_class_name_from_response_tag(response.tag)
            try:
                cls = globals().get(class_name)
                elements = response.getchildren()
                instance_list = []
                for element in elements:
                    single_instance = cls.from_xml(element)
                    instance_list.append(single_instance)
                instances[request_id] = instance_list
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error loading class for {class_name}: {e}")
        return instances

    def _break_response_into_single_instances(self, responses):
        instances = {}
        for response in responses:
            class_name = self._get_class_name_from_response_tag(response.tag)
            try:
                cls = globals().get(class_name)
                elements = response.getchildren()
                instance_list = []
                for element in elements:
                    single_instance = cls.from_xml(element)
                    instance_list.append(single_instance)
                instances[class_name] = instance_list
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error loading class for {class_name}: {e}")
        return instances

    def _break_response_into_plural_instances(self, responses):
        instances = self._break_response_into_single_instances(responses)
        plural_instances = []
        for class_name, list_of_instances in instances.items():
            try:
                cls = globals().get(class_name)
                plural_cls = globals().get(cls.Meta.plural_class_name)
                plural_instance = plural_cls.from_list(list_of_instances)
                plural_instances.append(plural_instance)
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error loading class for {class_name}: {e}")
        return plural_instances

    def _create_full_request(self, requestXML, encoding="utf-8"):
        """
        Combines converting the request to lxml and ensuring the proper structure for the XML request.

        :param requestXML: The input request, which may be a string, xml.etree.ElementTree.Element,
                           lxml.etree.Element, or a list of these types.
        :return: A properly structured lxml.etree.Element for sending to QuickBooks.
        """
        # Step 1: Convert the input to lxml if needed (handles lists too)
        requestXML = self._convert_to_lxml(requestXML)

        # Step 2: Ensure the QBXML structure
        QBXML, QBXMLMsgsRq = self._ensure_qbxml_structure(requestXML)

        # Step 3: Handle both single request and a list of requests
        if isinstance(requestXML, list):
            # Iterate through each request in the list
            i = 1
            for request in requestXML:
                # Ensure each request is properly converted to lxml
                request = self._convert_to_lxml(request)
                if request.get('requestID') is None:
                    request.attrib['requestID'] = str(i)
                QBXMLMsgsRq.append(request)
                i += 1
        else:
            # Single request handling
            if requestXML.get('requestID') is None:
                requestXML.attrib['requestID'] = "1"
            QBXMLMsgsRq.append(requestXML)

        declaration = f"""<?xml version="1.0" encoding="{encoding}"?><?qbxml version="{self.SDK_version}"?>"""
        full_request = declaration + et.tostring(QBXML, encoding=encoding).decode(encoding)
        logger.debug(f'full_request to go to qb: {full_request}')
        return full_request

    def _process_response(self, responseXML, response_type='raw_str'):
        """
        valid_response types can be one of the following:
            'raw_str' -> unedited response and the default response
            'response_list' -> a list of lxml.etree.Element objects representing the responses.
            'plural' -> a list of plural class instances
            'response_dict' -> a dictionary with the key being the request_id and the value being another dictionary with:
                    'status_code'
                    'status_severity'
                    'status_message'
                    'plural_instance'
            'instances_dict' -> a dict with the key being the main class and the value being a list of initialized classes.
            'none' -> response won't be returned
        """

        if response_type == 'raw_str':
            return responseXML
        elif response_type == 'none':
            return None
        else:
            QBXML = et.fromstring(responseXML)
            QBXMLMsgsRs = QBXML.find('QBXMLMsgsRs')
            if QBXMLMsgsRs is not None:
                responses = QBXMLMsgsRs.getchildren()
                if response_type == 'response_list':
                    return responses
                elif response_type == 'response_dict':
                    response_dict = self._create_response_dict_from_responses(responses)
                    return response_dict
                elif response_type == 'instances_dict':
                    instances = self._break_response_into_single_instances(responses)
                    return instances
                elif response_type == 'plural_list':
                    plural_instances = self._break_response_into_plural_instances(responses)
                    return plural_instances
                else:
                    return None
            else:
                return None

    def send_xml(self, requestXML, encoding="utf-8", is_full_request=False, response_type='raw_str'):
        """
        valid_response types can be one of the following:
            'raw_str' -> unedited response and the default response
            'response_list' -> a list of lxml.etree.Element objects representing the responses.
            'response_dict' -> a dictionary with the key being the request_id and the value being another dictionary with:
                    'statusCode'
                    'statusSeverity'
                    'statusMessage'
                    'response_list'
            'instances_dict' -> a dict with the key being the main class and the value being a list of initialized classes.
            'plural' -> a list of plural class instances
            'none' -> response won't be returned
        This method
            1. finishes the XML build
            2. ensures the XML request has key components
            3. sends the request to QuickBooks
        :param requestXML: The request element under the QBXMLMsgsRq tag.
        :return: responseXML from the quickbooks processor
        """

        if not is_full_request:
            full_request = self._create_full_request(requestXML, encoding)
        else:
            full_request = requestXML

        logger.debug(f'Opening connection to QuickBooks')
        if not self.qbXMLRP:
            self.qbXMLRP = self.dispatch()
            self.open_connection()
            self.begin_session()
        elif not self.session_begun:
            self.begin_session()
            print('open session')
        else:
            self.open_connection()
            self.begin_session()

        logger.debug(f'Connection to QuickBooks is open')
        try:
            responseXML = self.qbXMLRP.ProcessRequest(self.ticket, full_request)
        except Exception as e:
            easygui.msgbox(f"There was an error trying to send data to QuickBooks. Error: {e}", title="Error")
            if self.keep_session_open:
                pass
            elif self.keep_connection_open:
                self.qbXMLRP.EndSession()
            else:
                self.close_qb()
            logger.debug(e)
            return e

        if self.keep_session_open:
            pass
        elif self.keep_connection_open:
            self.qbXMLRP.EndSession()
        else:
            self.close_qb()

        response = self._process_response(responseXML, response_type)
        return response

    def __del__(self):
        try:
            self.close_qb()
        except Exception as e:
            logger.debug(e)

    def end_session(self):
        """
        Simply ends the QuickBooks Session.  This should ALWAYS happen before closing the program.
        :return: None
        """
        self.qbXMLRP.EndSession(self.ticket)
        self.session_begun = False

    def close_connection(self):
        """
        Simply closing the QuickBooks Connection.  This should ALWAYS happen before closing the program.
        :return: None
        """
        if self.session_begun:
            self.end_session()
        self.qbXMLRP.CloseConnection()
        self.connection_open = False

    def close_qb(self):
        """
       The purpose of this is to combine the end_session and close_connection into a single command.
       """
        self.end_session()
        self.close_connection()


class EasyGuiPopup:
    def __init__(self, message, title="Message"):
        self.message = message
        self.title = title
        self.stop_thread = False
        self.thread = threading.Thread(target=self.show)

    def show(self):
        while not self.stop_thread:
            easygui.msgbox(self.message, self.title)
            time.sleep(0.1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        # Give some time for the thread to stop
        time.sleep(0.2)


def create_address(dataclass_instance):
    address = Address()
    try:
        for field in fields(dataclass_instance):
            field_value = getattr(dataclass_instance, field.name)
            setattr(address, field.name, field_value)
        setattr(address, 'address_type', dataclass_instance.Meta.name)
        return address
    except Exception as e:
        return None


def xml_bool_to_py_bool(element):
    text = element.text.strip().lower() if element.text else None
    if text is None:
        return None
    elif text == 'true':
        return True
    elif text == 'false':
        return False
    else:
        raise ValueError("Invalid input; expected 'true' or 'false' in element text.")


# endregion


# region Core Mixins


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
            if field.name in ["Query", "Add", "Mod", "SpecialAccountAdd"]:
                pass
            else:
                value = getattr(self, field.name)
                if value is not None and not isinstance(value, type):
                    element = self._create_xml_element(root, field, value)
                    if element is not None and isinstance(element, list):
                        for el in element:
                            root.append(el)
                    elif element is not None:
                        root.append(element)
                    else:
                        pass
                else:
                    pass

        return root

    def to_xml_rq(self):
        root = self.to_xml()
        if self.Meta.name[-5:] == "Query":
            root.tag = str(self.Meta.name) + "Rq"
            return root
        elif self.Meta.name[-3:] == 'Add' or self.Meta.name[-3:] == 'Mod':
            rq = et.Element(str(self.Meta.name) + "Rq")
            rq.append(root)
            return rq
        else:
            raise NotImplementedError(f"Must Be Query, Add, or Mod Class: Class is {self.__class__.__name__}")

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
            #returned element needs to be the list of line_add's
            return element
        elif isinstance(value, bool):
            return self._handle_bool_value(field, value)
        elif isinstance(value, QBDates) or isinstance(value, QBTime) or isinstance(value, QBDateTime):
            return value.to_xml(field.name)
        elif is_dataclass(value):
            return value.to_xml()
        else:
            return self._handle_simple_value(field, value)

    def _handle_list_value(self, root, field, list_of_objs_or_elements):
        """
        Handle list values, creating XML elements for each item in the list.
        """
        if len(list_of_objs_or_elements) == 0:
            return None
        list_of_elements = []
        for obj in list_of_objs_or_elements:
            if isinstance(obj, et._Element):
                #the object is already an lxml element and can be added directly to the parent.
                list_of_elements.append(obj)
            else:
                element = obj.to_xml()
                list_of_elements.append(element)
        return list_of_elements

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
    def _ensure_lxml_type(element):
        if isinstance(element, et._Element):
            return element
        elif isinstance(element, ETree.Element):
            element = et.fromstring(et.tostring(element))
        elif isinstance(element, str):
            element = et.fromstring(element)
        else:
            raise TypeError(
                f"Invalid type {type(element)}. Expected lxml.etree._Element, xml.etree.ElementTree.Element, or str.")

        return element

    @staticmethod
    def _get_field_type(field):
        field_type = field.type
        if get_origin(field_type) is Union:
            # Handle Optional and Union types
            field_type = next(arg for arg in get_args(field_type) if arg is not type(None))
            return field_type
        else:
            return field_type

    @staticmethod
    def _parse_list_field_type(init_args, field, field_type, an_xml_list_element):
        instance = field_type.__args__[0].from_xml(an_xml_list_element)
        if field.name in init_args.keys():
            if isinstance(init_args[field.name], list):
                init_args[field.name].append(instance)
            else:
                # if it's not a list then what is it?
                pass
        else:
            init_args[field.name] = [instance]
        return init_args


    @classmethod
    def _parse_field_according_to_type(cls, init_args, field, field_type, xml_element):
        # Check if the field type is a dataclass
        if is_dataclass(field_type):
            init_args[field.name] = field_type.from_xml(xml_element)
        elif hasattr(field_type, '_name') and field_type._name == 'List':
            init_args = cls._parse_list_field_type(init_args, field, field_type, xml_element)
        elif field.name in cls.IS_YES_NO_FIELD_LIST:
            init_args[field.name] = yes_no_dict[xml_element.text]
        elif field_type == bool:
            init_args[field.name] = xml_bool_to_py_bool(xml_element)
        else:
            try:
                init_args[field.name] = field_type(xml_element.text)
            except Exception as e:
                logger.debug(e)
                raise ValueError(e)
        return init_args

    @classmethod
    def _get_init_args(cls, element, field_names):
        init_args = {}
        for xml_element in element:
            field_name = xml_element.tag
            if field_name in field_names:
                field = field_names[field_name]
                field_type = cls._get_field_type(field)
                init_args = cls._parse_field_according_to_type(init_args, field, field_type, xml_element)
            else:
                try:
                    logger.debug(f'Extra field {field_name} is in the xml provided')
                except Exception as e:
                    print(e)
        return init_args

    @classmethod
    def from_xml(cls, element: et.Element) -> Any:
        element = cls._ensure_lxml_type(element)

        field_names = {field.metadata.get("name", field.name): field for field in cls.__dataclass_fields__.values()}
        init_args = cls._get_init_args(element, field_names)

        if element is not None and not len(element) and element.text is not None and len(element.text) and element.text.replace('\n', '').strip() != '':
            # The element exists, is not a list, has a name and is not a new line.

            if len(cls.__dataclass_fields__):
                #a dataclass to parse out
                main_field = next(iter(cls.__dataclass_fields__.values()))
                init_args[main_field.name] = element.text
            elif element.tag in ['InvoiceLineRet']:
                for line in element:
                    invoice_line = InvoiceLine.from_xml(line)
                    return invoice_line
            else:
                pass
        else:
            #Normal Element to be parsed out
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


class CreateAddOrModFromParentMixin:


    def _handle_ref_subvalue(self, value, attr, attrs_that_are_ids):
        for ref_attr, ref_value in vars(value).items():
            if ref_attr in attrs_that_are_ids:
                setattr(value, ref_attr, None)
            else:
                pass
        setattr(self, attr, value)


    def _handle_regular_sub_value(self, attr, value, keep_ids):
        attrs_that_are_ids = ["list_id", "txn_line_id", "txn_id"]
        if attr in ["Query", "Add", "Mod", "SpecialAccountAdd"]:
            pass
        elif keep_ids:
            setattr(self, attr, value)
        elif attr[-3:] == 'ref':
            self._handle_ref_subvalue(value, attr, attrs_that_are_ids)
        elif attr in attrs_that_are_ids:
            pass
        elif attr[-2:] == '_id':
            setattr(value, attr, None)
        else:
            setattr(self, attr, value)


    def _handle_list_sub_instance(self, attr, sub_instance_list, add_or_mod, keep_ids):
        converted_sub_instances = []
        for sub_instance in sub_instance_list:
            add_or_mod_class = getattr(sub_instance, add_or_mod)
            if isinstance(add_or_mod_class, str) and add_or_mod_class == 'self':
                # Special instance where the Add class is actually itself instead of a separate class
                converted_sub_instance = sub_instance.__class__.create_add_or_mod_from_parent(sub_instance, add_or_mod, keep_ids=keep_ids)
            else:
                # Add class is already assigned
                converted_sub_instance = add_or_mod_class.create_add_or_mod_from_parent(sub_instance, add_or_mod)
            converted_sub_instances.append(converted_sub_instance)
        if converted_sub_instances:
            setattr(self, attr, converted_sub_instances)
        else:
            pass


    @classmethod
    def create_add_or_mod_from_parent(cls, parent, add_or_mod, keep_ids=True):
        """add_or_mod can be 'add' or 'mod' """
        assert add_or_mod in ['Add', 'Mod'], "add_or_mod must be 'add' or 'mod'"
        instance = cls()
        for attr, value in parent.__dict__.items():
            if value is None:
                pass
            elif hasattr(instance, attr):
                if isinstance(value, list):
                    instance._handle_list_sub_instance(attr, value, add_or_mod, keep_ids)
                else:
                    instance._handle_regular_sub_value(attr, value, keep_ids)
            else:
                pass
        if getattr(instance, 'validate', False):
            instance.validate()
        else:
            pass
        return instance


class QBQueryMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}QueryRq"


class QBAddRqMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CreateAddOrModFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}AddRq"


class QBModRqMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CreateAddOrModFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}ModRq"


class QBAddMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CreateAddOrModFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}Add"


class QBModMixin(MaxLengthMixin, ToXmlMixin, ValidationMixin, CreateAddOrModFromParentMixin, ReprMixin):

    @classmethod
    def set_name(cls, name):
        cls.Meta.name = f"{name}Mod"


class SaveMixin:

    def _get_mod_rq_xml(self):
        mod_class = getattr(self, f'Mod', None)
        mod_instance = mod_class.create_add_or_mod_from_parent(self, add_or_mod='Mod')
        mod_xml = mod_instance.to_xml()
        rq_element_name = mod_class.__name__ + 'Rq'
        rq_element = et.Element(rq_element_name)
        rq_element.append(mod_xml)
        return rq_element

    def _get_add_rq_xml(self):
        add_class = getattr(self, f'Add', None)
        add_instance = add_class.create_add_or_mod_from_parent(self, add_or_mod='Add')
        add_xml = add_instance.to_xml()
        rq_element_name = add_class.__name__ + 'Rq'
        rq_element = et.Element(rq_element_name)
        rq_element.append(add_xml)
        return rq_element

    def save_as_new(self, qb):
        add_xml = self._get_add_rq_xml()
        response = qb.send_xml(add_xml)
        return response

    def save(self, qb):
        if hasattr(self, 'list_id') and self.list_id is not None:
            mod_xml = self._get_mod_rq_xml()
            response = qb.send_xml(mod_xml)
            return response
        elif hasattr(self, 'txn_id') and self.txn_id is not None:
            mod_xml = self._get_mod_rq_xml()
            response = qb.send_xml(mod_xml)
            return response
        else:
            response = self.save_as_new(qb)
            return response


class QBMixin(MaxLengthMixin, ToXmlMixin, FromXmlMixin, ValidationMixin, CreateAddOrModFromParentMixin, ReprMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


class QBMixinWithSave(QBMixin, SaveMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


class PluralMixin:

    class Meta:
        name = ''
        plural_of = ''
        plural_of_db_model = ''

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
    def from_list(cls, items):
        instance = cls()
        for item in items:
            instance.add_item(item)
        return instance

    @classmethod
    def get_all_from_qb(cls, qb, include_custom_fields=False, include_line_items=False, include_linked_txns=False):
        QueryRq = et.Element(f'{cls.Meta.name}QueryRq')
        if include_line_items:
            custom_query = et.SubElement(QueryRq, 'IncludeLineItems')
            custom_query.text = 'true'
        else:
            pass

        if include_linked_txns:
            custom_query = et.SubElement(QueryRq, 'IncludeLinkedTxns')
            custom_query.text = 'true'
        else:
            pass

        if include_custom_fields:
            custom_query = et.SubElement(QueryRq, 'OwnerID')
            custom_query.text = '0' #zero is the ownerID for all custom fields (not private fields)
        else:
            pass

        QueryRs_list = qb.send_xml(QueryRq)
        if type(QueryRs_list) == list and len(QueryRs_list) == 1:
            QueryRs = QueryRs_list[0]
            plural_instance = cls()
            for Ret in QueryRs:
                obj = plural_instance.Meta.plural_of.from_xml(Ret)
                plural_instance._items.append(obj)
            return plural_instance
        else:
            logger.debug(f"QueryRs_list is of type {type(QueryRs_list)} instead of list type")

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
                plural_instance.add_item(plural_of_instance)
            return plural_instance

    @classmethod
    def __get_last_time_modified(cls, qb_max_time_modified, qb):
        plural_instance = cls()
        query = plural_instance.Meta.plural_of.Query()
        query.from_modified_date = qb_max_time_modified
        query_xml = query.to_xml()
        QueryRs = qb.send_xml(query_xml)
        for Ret in QueryRs:
            obj = plural_instance.Meta.plural_of.from_xml(Ret)
            plural_instance._items.append(obj)
        return plural_instance

    # @classmethod
    # def update_db(cls, qb, session):
    #     qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
    #     plural_instance = cls.__get_last_time_modified(qb_max_time_modified, qb)
    #     plural_instance.to_db(session)
    #
    # @classmethod
    # def populate_db(cls, qb, session):
    #     instances = cls.get_all_from_qb(qb)
    #     instances.to_db(session)
    #
    # @classmethod
    # def populate_or_update_db(cls, qb, session):
    #     qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
    #     if qb_max_time_modified:
    #         cls.update_db(qb, session)
    #     else:
    #         cls.populate_db(qb, session)

    def to_xml(self):
        """
        Converts all items in the plural mixin into a list of lxml elements
        by calling each child's `to_xml` method.
        """
        xml_elements = []
        for item in self._items:
            xml_element = item.to_xml()  # Each item must implement `to_xml`
            xml_elements.append(xml_element)
        return xml_elements

    def to_add_xml(self):
        """
        Converts all items in the plural mixin into a list of add lxml elements
        by calling each child's `to_xml` method.
        """
        xml_elements = []
        for item in self._items:
            add_cls = getattr(item, 'Add', None)
            add_instance = add_cls.create_add_or_mod_from_parent(item, 'Add', keep_ids=False)
            xml_element = add_instance.to_xml_rq()
            xml_elements.append(xml_element)
        return xml_elements

    def _create_data_ext_mod(self, add_response):
        xml_elements = []
        start_request_id = 100
        for item in self._items:
            request_id = start_request_id/100
            data_ext = getattr(item, 'Add', None)
            add_instance = add_cls.create_add_or_mod_from_parent(item, 'Add', keep_ids=False)
            xml_element = add_instance.to_xml_rq()
            xml_elements.append(xml_element)
        return xml_elements

    def to_xml_file(self, file_path: str) -> None:
        """
        Generates an XML file with the plural objects.
        Creates a root element based on the Meta class name, appends all items, and writes to the file path.

        Args:
            file_path (str): The path of the file to write the XML to. The file will be replaced if it exists.
        """

        list_of_xml = self.to_xml()
        root = et.Element(f"{self.Meta.name}QueryRs")
        for xml_element in list_of_xml:
            root.append(xml_element)
        xml_str = et.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
        with open(file_path, "w") as file:
            file.write(xml_str)
        logger.debug('Finished to_xml_file')


class PluralListSaveMixin:
    def save_all(self, qb, raw_response=False):
        xml_requests = []
        for item in self:
            if item.list_id is not None:
                mod_xml = item._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = item._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests, response_type=raw_response)
        return response

    def add_all(self, qb, raw_response=False):
        xml_requests = []
        for item in self:
            add_xml = item._get_add_rq_xml()
            xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests, response_type=raw_response)
        return response


class PluralTrxnSaveMixin:

    def _set_ids_to_none(self, id_name):
        # Iterate over each item in the _items list, assuming they are instances of some class
        for item in self:
            self._set_list_id_in_instance_to_none(item, id_name)

    def _set_list_id_in_instance_to_none(self, obj, id_name):
        # Iterate through all attributes of the object
        for attr_name in dir(obj):
            if attr_name.startswith('__'):
                pass
            elif attr_name.startswith('_'):
                pass
            elif attr_name in ['Add', 'Mod', 'Query', 'Meta', 'IS_YES_NO_FIELD_LIST']:
                pass
            elif attr_name.endswith('Ref') or attr_name.endswith('ref'):
                ref = getattr(obj, attr_name)
                if hasattr(ref, id_name):
                    ref.list_id = None
                else:
                    pass
            else:
                attr_value = getattr(obj, attr_name)

                # If the attribute is a list, iterate through the list items
                if isinstance(attr_value, list):
                    for sub_item in attr_value:
                        if hasattr(sub_item, id_name):
                            setattr(sub_item, id_name, None)
                        else:
                            pass
                        self._set_list_id_in_instance_to_none(sub_item, id_name)  # Recurse for nested objects

                # If the attribute itself has a 'list_id', set it to None
                elif hasattr(attr_value, id_name):
                    setattr(attr_value, id_name, None)

                else:

                    # If the attribute is 'list_id', set it to None
                    if attr_name == id_name:
                        setattr(obj, attr_name, None)
                    else:
                        pass

    # def _index_data_ext(self):
    #     data_ext_dict = {}
    #     for trxn in self:
    #         if hasattr(trxn, 'data_ext') and len(trxn.data_ext):
    #             data_ext_dict[trxn] = {index: ext for index, ext in enumerate(trxn.data_ext, start=1)}
    #     return data_ext_dict
    #
    # def _create_data_ext_mod_requests(self, response):
    #     data_ext_dict = self._index_data_ext()
    #
    #
    # def _handle_data_ext_with_add_request(self, response, qb):
    #     data_ext_mod_request = self._create_data_ext_mod_requests(response)
    #     data_ext_mod_response = qb.send_xml(data_ext_mod_request, response_type='raw_response')

    def save_all(self, qb, raw_response=False):
        xml_requests = []
        for trxn in self:
            if trxn.trxn_id is not None:
                mod_xml = trxn._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = trxn._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests, response_type=raw_response)
        return response

    def add_all(self, qb, raw_response=False):
        xml_requests = []
        for trxn in self:
            add_xml = trxn._get_add_rq_xml()
            xml_requests.append(add_xml)

        response = qb.send_xml(xml_requests, response_type='')
        self._handle_data_ext_with_add_request(response, qb)
        return response





@dataclass
class QBRefMixin(QBMixin):

    list_id: Optional[str] = list_id
    full_name: Optional[str] = full_name

# endregion


# region Refs


@dataclass
class TermsRef(QBRefMixin):
    class Meta:
        name = "TermsRef"


@dataclass
class VendorTypeRef(QBRefMixin):
    class Meta:
        name = "VendorTypeRef"


@dataclass
class VendorRef(QBRefMixin):
    class Meta:
        name = "VendorRef"


@dataclass
class PrefVendorRef(QBRefMixin):
    class Meta:
        name = "PrefVendorRef"


@dataclass
class TaxVendorRef(QBRefMixin):
    class Meta:
        name = "TaxVendorRef"


@dataclass
class OverrideUomsetRef(QBRefMixin):

    class Meta:
        name = "OverrideUomsetRef"


@dataclass
class TemplateRef(QBRefMixin):

    class Meta:
        name = "TemplateRef"


@dataclass
class ShipMethodRef(QBRefMixin):

    class Meta:
        name = "ShipMethodRef"


@dataclass
class ItemPurchaseTaxRef(QBRefMixin):
    class Meta:
        name = "ItemPurchaseTaxRef"

@dataclass
class PurchaseTaxCodeRef(QBRefMixin):
    class Meta:
        name = "PurchaseTaxCodeRef"


@dataclass
class SalesTaxCodeRef(QBRefMixin):
    class Meta:
        name = "SalesTaxCodeRef"


@dataclass
class ItemSalesTaxRef(QBRefMixin):
    class Meta:
        name = "ItemSalesTaxRef"


@dataclass
class SalesRepEntityRef(QBRefMixin):
    class Meta:
        name = "SalesRepEntityRef"


@dataclass
class SalesRepRef(QBRefMixin):
    class Meta:
        name = "SalesRepRef"


@dataclass
class PriceLevelRef(QBRefMixin):

    class Meta:
        name = "PriceLevelRef"


@dataclass
class PayrollItemWageRef(QBRefMixin):
    class Meta:
        name = "PayrollItemWage"


@dataclass
class OtherNameRef(QBRefMixin):
    class Meta:
        name = "OtherNameRef"


@dataclass
class PaymentMethodRef(QBRefMixin):

    class Meta:
        name = "PaymentMethodRef"


@dataclass
class JobTypeRef(QBRefMixin):
    class Meta:
        name = "JobTypeRef"


@dataclass
class RefundFromAccountRef(QBRefMixin):
    class Meta:
        name = "RefundFromAccountRef"


@dataclass
class CogsaccountRef(QBRefMixin):
    class Meta:
        name = "CogsaccountRef"

@dataclass
class AssetAccountRef(QBRefMixin):
    class Meta:
        name = "AssetAccountRef"


@dataclass
class OverrideItemAccountRef(QBRefMixin):
    class Meta:
        name = "OverrideItemAccountRef"


@dataclass
class AraccountRef(QBRefMixin):
    class Meta:
        name = "AraccountRef"


@dataclass
class DepositToAccountRef(QBRefMixin):
    class Meta:
        name = "DepositToAccountRef"


@dataclass
class ExpenseAccountRef(QBRefMixin):
    class Meta:
        name = "ExpenseAccountRef"


@dataclass
class IncomeAccountRef(QBRefMixin):
    class Meta:
        name = "IncomeAccountRef"

@dataclass
class AccountRef(QBRefMixin):
    class Meta:
        name = "AccountRef"


@dataclass
class PrefillAccountRef(QBRefMixin):
    class Meta:
        name = "PrefillAccountRef"


@dataclass
class ApaccountRef(QBRefMixin):
    class Meta:
        name = "ApaccountRef"


@dataclass
class BankAccountRef(QBRefMixin):
    class Meta:
        name = "BankAccountRef"


@dataclass
class CreditCardAccountRef(QBRefMixin):
    class Meta:
        name = "CreditCardAccountRef"


@dataclass
class DepositToAccountRef(QBRefMixin):
    class Meta:
        name = "DepositToAccountRef"


@dataclass
class TransferFromAccountRef(QBRefMixin):
    class Meta:
        name = "TransferFromAccountRef"


@dataclass
class TransferToAccountRef(QBRefMixin):
    class Meta:
        name = "TransferToAccountRef"

@dataclass
class PayeeEntityRef(QBRefMixin):
    class Meta:
        name = "PayeeEntityRef"


@dataclass
class AdditionalContactRef(QBRefMixin):
    class Meta:
        name = "AdditionalContactRef"

    contact_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactName",
            "type": "Element",
            "required": True,
            "max_length": 40
        },
    )
    contact_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactValue",
            "type": "Element",
            "required": True,
            "max_length": 255
        },
    )


@dataclass
class ParentRef(QBRefMixin):

    class Meta:
        name = "ParentRef"


@dataclass
class ListObjRef(QBRefMixin):

    class Meta:
        name = "ListObjRef"


@dataclass
class SalesTaxReturnLineRef(QBRefMixin):

    class Meta:
        name = "SalesTaxReturnLineRef"


@dataclass
class PreferredPaymentMethodRef(QBRefMixin):

    class Meta:
        name = "PreferredPaymentMethodRef"


@dataclass
class JobTypeRef(QBRefMixin):

    class Meta:
        name = "JobTypeRef"


@dataclass
class DiscountAccountRef(QBRefMixin):
    class Meta:
        name = "DiscountAccountRef"


@dataclass
class DiscountClassRef(QBRefMixin):
    class Meta:
        name = "DiscountClassRef"


@dataclass
class BillingRateRef(QBRefMixin):

    class Meta:
        name = "BillingRateRef"


@dataclass
class ClassInQBRef(QBRefMixin):
    class Meta:
        name = "ClassRef"


@dataclass
class OverrideClassRef(QBRefMixin):
    class Meta:
        name = "OverrideClassRef"


@dataclass
class CurrencyRef(QBRefMixin):
    class Meta:
        name = "CurrencyRef"


@dataclass
class CustomerMsgRef(QBRefMixin):

    class Meta:
        name = "CustomerMsgRef"


@dataclass
class CustomerRef(QBRefMixin):
    class Meta:
        name = "CustomerRef"


@dataclass
class CustomerTypeRef(QBRefMixin):
    class Meta:
        name = "CustomerTypeRef"


@dataclass
class EntityRef(QBRefMixin):
    class Meta:
        name = "EntityRef"


@dataclass
class SupervisorRef(QBRefMixin):
    class Meta:
        name = "SupervisorRef"


@dataclass
class PayrollItemWageRef(QBRefMixin):
    class Meta:
        name = "PayrollItemWageRef"


@dataclass
class InventorySiteRef(QBRefMixin):

    class Meta:
        name = "InventorySiteRef"


@dataclass
class ParentSiteRef(QBRefMixin):

    class Meta:
        name = "ParentSiteRef"


@dataclass
class InventorySiteLocationRef(QBRefMixin):

    class Meta:
        name = "InventorySiteLocationRef"


@dataclass
class UnitOfMeasureSetRef(QBRefMixin):
    class Meta:
        name = "UnitOfMeasureSetRef"


@dataclass
class ItemRef(QBRefMixin):
    class Meta:
        name = "ItemRef"


@dataclass
class ItemInventoryAssemblyRef(QBRefMixin):
    class Meta:
        name = "ItemInventoryAssemblyRef"


@dataclass
class ItemGroupRef(QBRefMixin):
    class Meta:
        name = "ItemGroupRef"


@dataclass
class ItemServiceRef(QBRefMixin):
    class Meta:
        name = "ItemServiceRef"


@dataclass
class ItemSalesTaxRef(QBRefMixin):
    class Meta:
        name = "ItemSalesTaxRef"


@dataclass
class ItemInventoryRef(QBRefMixin):
    class Meta:
        name = "ItemInventoryRef"


# endregion


# region Common


@dataclass
class TxnLineDetail(QBMixin):
    class Meta:
        name = "TxnLineDetail"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class AddressBlock(QBMixin):
    class Meta:
        name = "AddressBlock"

    addr1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr1",
            "type": "Element",
            "max_length": 41
        },
    )
    addr2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr2",
            "type": "Element",
            "max_length": 41
        },
    )
    addr3: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr3",
            "type": "Element",
            "max_length": 41
        },
    )
    addr4: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr4",
            "type": "Element",
            "max_length": 41
        },
    )
    addr5: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr5",
            "type": "Element",
            "max_length": 41
        },
    )

@dataclass
class BillAddressBlock(AddressBlock):
    class Meta:
        name = "BillAddressBlock"

@dataclass
class OtherNameAddressBlock(AddressBlock):
    class Meta:
        name = "OtherNameAddressBlock"

@dataclass
class VendorAddressBlock(AddressBlock):
    class Meta:
        name = "VendorAddressBlock"

@dataclass
class ShipAddressBlock(AddressBlock):
    class Meta:
        name = "ShipAddressBlock"

@dataclass
class Address(AddressBlock):
    class Meta:
        name = "Address"

    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "max_length": 31
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "max_length": 21
        },
    )
    postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "max_length": 13
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "max_length": 31
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "max_length": 41
        },
    )

@dataclass
class EmployeeAddress(AddressBlock):
    class Meta:
        name = "EmployeeAddress"

    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "max_length": 31
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "max_length": 21
        },
    )
    postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "max_length": 13
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "max_length": 31
        },
    )

@dataclass
class BillAddress(Address):
    class Meta:
        name = "BillAddress"

@dataclass
class ShipAddress(Address):
    class Meta:
        name = "ShipAddress"

@dataclass
class OtherNameAddress(Address):
    class Meta:
        name = "OtherNameAddress"


@dataclass
class VendorAddress(Address):
    class Meta:
        name = "VendorAddress"

@dataclass
class ShipToAddress(Address):
    class Meta:
        name = "ShipToAddress"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41
        },
    )
    default_ship_to: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DefaultShipTo",
            "type": "Element"
        },
    )


@dataclass
class Contacts(QBMixin):
    class Meta:
        name = "Contacts"

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
            "required": True
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
            "required": True
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "required": True,
            "max_length": 25
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 5
        },
    )

@dataclass
class ContactsMod(QBMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Salutation", "FirstName", "MiddleName",
        "LastName", "JobTitle", "AdditionalContactRef"
    ]
    class Meta:
        name = "ContactsMod"


    list_id: Optional[str] = list_id
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "required": True,
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 5,
        },
    )

@dataclass
class AdditionalNotes(QBMixin):
    class Meta:
        name = "AdditionalNotes"

    note_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteID",
            "type": "Element",
            "required": True,
        },
    )
    date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "required": True,
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "required": True,
            "max_length": 4095,
        },
    )

@dataclass
class AdditionalNotesMod(QBMixin):

    class Meta:
        name = "AdditionalNotesMod"

    note_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteID",
            "type": "Element",
            "required": True,
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "required": True,
            "max_length": 4095,
        },
    )


@dataclass
class AdditionalNotesRet(QBMixin):
    class Meta:
        name = "AdditionalNotesRet"

    note_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteID",
            "type": "Element",
            "required": True,
        },
    )
    date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "required": True,
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "required": True,
            "max_length": 4095,
        },
    )


@dataclass
class DataExtAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "OwnerID", "DataExtName", "ListDataExtType", "ListObjRef",
        "TxnDataExtType", "TxnID", "TxnLineID", "OtherDataExtType", "DataExtValue"
    ]

    class Meta:
        name = "DataExtAdd"

    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
            "required": True,
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
    list_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListDataExtType",
            "type": "Element",
            "valid_values": VALID_LIST_DATA_EXT_TYPE_VALUES
        },
    )
    list_obj_ref: Optional[ListObjRef] = field(
        default=None,
        metadata={
            "name": "ListObjRef",
            "type": "Element",
        },
    )
    txn_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDataExtType",
            "type": "Element",
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES,
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    other_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherDataExtType",
            "type": "Element",
            "valid_values": ["Company"]
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
class DataExtMod(QBAddRqMixin):
    FIELD_ORDER = [
        "OwnerID", "DataExtName", "ListDataExtType", "ListObjRef",
        "TxnDataExtType", "TxnID", "TxnLineID", "OtherDataExtType", "DataExtValue"
    ]

    class Meta:
        name = "DataExtMod"

    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
            "required": True,
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
    list_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListDataExtType",
            "type": "Element",
            "valid_values": VALID_LIST_DATA_EXT_TYPE_VALUES
        },
    )
    list_obj_ref: Optional[ListObjRef] = field(
        default=None,
        metadata={
            "name": "ListObjRef",
            "type": "Element",
        },
    )
    txn_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDataExtType",
            "type": "Element",
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES,
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    other_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherDataExtType",
            "type": "Element",
            "valid_values": ["Company"]
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
class DataExt(QBMixin):

    class Meta:
        name = "DataExtRet"

    #There is no Query
    Add: Type[DataExtAdd] = DataExtAdd
    Mod: Type[DataExtMod] = DataExtMod

    owner_id: Optional[str] = field(
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
    data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtType",
            "type": "Element",
            "required": True,
            "valid_values": ["AMTTYPE", "DATETIMETYPE", "INTTYPE", "PERCENTTYPE", "PRICETYPE", "QUANTYPE", "STR1024TYPE", "STR255TYPE"],
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
class SetCredit(QBMixin):

    class Meta:
        name = "SetCredit"

    credit_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditTxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    applied_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
            "required": True,
        },
    )
    override: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Override",
            "type": "Element",
        },
    )


@dataclass
class LinkedTxn(QBMixin):

    class Meta:
        name = "LinkedTxn"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "required": True,
            "valid_values": VALID_TXN_TYPE_VALUES,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
            "required": True,
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "LinkType",
            "type": "Element",
            "valid_values": ["AMTTYPE", "QUANTYPE"]
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )


@dataclass
class CreditCardInfo(QBMixin):
    FIELD_ORDER = [
        "CreditCardNumber", "ExpirationMonth", "ExpirationYear", "NameOnCard",
        "CreditCardAddress", "CreditCardPostalCode"
    ]

    class Meta:
        name = "CreditCardInfo"

    credit_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    expiration_month: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationMonth",
            "type": "Element",
            "valid_values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        },
    )
    expiration_year: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationYear",
            "type": "Element",
        },
    )
    name_on_card: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCard",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardAddress",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardPostalCode",
            "type": "Element",
            "max_length": 41,
        },
    )


@dataclass
class CurrencyFilter(QBRefMixin):
    # I know it doesn't set Ref in the name but it's a Ref
    class Meta:
        name = "CurrencyFilter"

@dataclass
class NameFilter(ToXmlMixin):

    class Meta:
        name = "NameFilter"

    match_criterion: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatchCriterion",
            "type": "Element",
            "required": True,
            "valid_values": ["StartsWith", "Contains", "EndsWith"]

        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class NameRangeFilter(ToXmlMixin):

    class Meta:
        name = "NameRangeFilter"

    from_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FromName",
            "type": "Element",
        },
    )
    to_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToName",
            "type": "Element",
        },
    )





@dataclass
class TotalBalanceFilter(ToXmlMixin):

    class Meta:
        name = "TotalBalanceFilter"

    operator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Element",
            "required": True,
            "valid_values": VALID_OPERATOR_VALUES
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class ClassFilter(ToXmlMixin):

    class Meta:
        name = "ClassFilter"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class ModifiedDateRangeFilter(ToXmlMixin):

    class Meta:
        name = "ModifiedDateRangeFilter"

    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )

@dataclass
class TxnDateRangeFilter(ToXmlMixin):

    class Meta:
        name = "TxnDateRangeFilter"

    from_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromTxnDate",
            "type": "Element",
        },
    )
    to_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToTxnDate",
            "type": "Element",
        },
    )
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )

    def __post_init__(self):
        # Validate that from_txn_date and to_txn_date have date_is_macro as False
        if self.from_txn_date and self.from_txn_date.date_is_macro:
            raise ValueError("from_txn_date cannot be a macro date.")

        if self.to_txn_date and self.to_txn_date.date_is_macro:
            raise ValueError("to_txn_date cannot be a macro date.")

        # Validate that date_macro has date_is_macro as True
        if self.date_macro and not self.date_macro.date_is_macro:
            raise ValueError("date_macro must be a macro date.")


@dataclass
class EntityFilter(ToXmlMixin):

    class Meta:
        name = "EntityFilter"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class AccountFilter(ToXmlMixin):

    class Meta:
        name = "AccountFilter"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class RefNumberFilter(ToXmlMixin):

    class Meta:
        name = "RefNumberFilter"

    match_criterion: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatchCriterion",
            "type": "Element",
            "required": True,
            "valid_values": ["StartsWith", "Contains", "EndsWith"]
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class RefNumberRangeFilter(ToXmlMixin):

    class Meta:
        name = "RefNumberRangeFilter"

    from_ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "FromRefNumber",
            "type": "Element",
        },
    )
    to_ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToRefNumber",
            "type": "Element",
        },
    )

@dataclass
class ItemFilter(ToXmlMixin):

    class Meta:
        name = "ItemFilter"

    list_ids: List[str] = list_ids
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159,
        },
    )
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
            "max_length": 159,
        },
    )


@dataclass
class CreditCardTxnInputInfo(QBMixin):

    class Meta:
        name = "CreditCardTxnInputInfo"

    credit_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardNumber",
            "type": "Element",
            "required": True,
            "max_length": 25,
        },
    )
    expiration_month: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationMonth",
            "type": "Element",
            "required": True,
            "valid_values": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        },
    )
    expiration_year: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationYear",
            "type": "Element",
            "required": True,
        },
    )
    name_on_card: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCard",
            "type": "Element",
            "required": True,
            "max_length": 41,
        },
    )
    credit_card_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardAddress",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardPostalCode",
            "type": "Element",
            "max_length": 18,
        },
    )
    commercial_card_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CommercialCardCode",
            "type": "Element",
            "max_length": 24,
        },
    )
    transaction_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionMode",
            "type": "Element",
            "valid_values": ["CardNotPresent", "CardPresent"]
        },
    )
    credit_card_txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnType",
            "type": "Element",
            "valid_values": ["Authorization", "Capture", "Charge", "Refund", "VoiceAuthorization"]
        },
    )


@dataclass
class CreditCardTxnResultInfo(QBMixin):

    class Meta:
        name = "CreditCardTxnResultInfo"

    result_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "ResultCode",
            "type": "Element",
            "required": True,
        },
    )
    result_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultMessage",
            "type": "Element",
            "required": True,
            "max_length": 60,
        },
    )
    credit_card_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTransID",
            "type": "Element",
            "required": True,
            "max_length": 24,
        },
    )
    merchant_account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "MerchantAccountNumber",
            "type": "Element",
            "required": True,
            "max_length": 32,
        },
    )
    authorization_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuthorizationCode",
            "type": "Element",
            "max_length": 12,
        },
    )
    avsstreet: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSStreet",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    avszip: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSZip",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    card_security_code_match: Optional[str] = field(
        default=None,
        metadata={
            "name": "CardSecurityCodeMatch",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    recon_batch_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReconBatchID",
            "type": "Element",
            "max_length": 84,
        },
    )
    payment_grouping_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "PaymentGroupingCode",
            "type": "Element",
        },
    )
    payment_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentStatus",
            "type": "Element",
            "required": True,
            "valid_values": ["Unknown", "Completed"],
        },
    )
    txn_authorization_time: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationTime",
            "type": "Element",
            "required": True,
        },
    )
    txn_authorization_stamp: Optional[int] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationStamp",
            "type": "Element",
        },
    )
    client_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientTransID",
            "type": "Element",
            "max_length": 16,
        },
    )


@dataclass
class CreditCardTxnInfo(QBMixin):
    class Meta:
        name = "CreditCardTxnInfo"

    credit_card_txn_input_info: Optional[CreditCardTxnInputInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInputInfo",
            "type": "Element",
            "required": True,
        },
    )
    credit_card_txn_result_info: Optional[CreditCardTxnResultInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnResultInfo",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SetCreditCreditTxnId(QBMixin):
    class Meta:
        name = "SetCreditCreditTxnId"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 36,
        },
    )
    use_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "useMacro",
            "type": "Attribute",
        },
    )

@dataclass
class SetCredit(QBMixin):

    class Meta:
        name = "SetCredit"

    credit_txn_id: Optional[SetCreditCreditTxnId] = field(
        default=None,
        metadata={
            "name": "CreditTxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    applied_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
            "required": True,
        },
    )
    override: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Override",
            "type": "Element",
        },
    )

@dataclass
class AppliedToTxnAdd(QBMixin):
    FIELD_ORDER = [
        "TxnID", "PaymentAmount", "SetCredit", "DiscountAmount",
        "DiscountAccountRef", "DiscountClassRef"
    ]

    class Meta:
        name = "AppliedToTxnAdd"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    payment_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PaymentAmount",
            "type": "Element",
        },
    )
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )


@dataclass
class AppliedToTxnMod(QBMixin):
    FIELD_ORDER = [
        "TxnID", "PaymentAmount", "SetCredit", "DiscountAmount",
        "DiscountAccountRef", "DiscountClassRef"
    ]

    class Meta:
        name = "AppliedToTxnMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    payment_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PaymentAmount",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )


@dataclass
class AppliedToTxn(QBMixin):
    FIELD_ORDER = [
        "TxnID", "TxnType", "TxnDate", "RefNumber", "BalanceRemaining",
        "Amount", "DiscountAmount", "DiscountAccountRef",
        "DiscountClassRef", "LinkedTxn"
    ]

    class Meta:
        name = "AppliedToTxn"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "required": True,
            "valid_values": VALID_TXN_TYPE_VALUES
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    balance_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )


@dataclass
class RefundAppliedToTxnAdd(QBMixin):
    class Meta:
        name = "RefundAppliedToTxnAdd"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    refund_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RefundAmount",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RefundAppliedToTxn(QBMixin):
    class Meta:
        name = "RefundAppliedToTxnAdd"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge",
                "CreditCardCredit", "CreditMemo", "Deposit", "Estimate",
                "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
                "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck",
                "PurchaseOrder", "ReceivePayment", "SalesOrder", "SalesReceipt",
                "SalesTaxPaymentCheck", "Transfer", "VendorCredit", "YTDAdjustment"
            ],
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
            "required": True,
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    credit_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemaining",
            "type": "Element",
            "required": True,
        },
    )
    refund_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RefundAmount",
            "type": "Element",
            "required": True,
        },
    )
    credit_remaining_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemainingInHomeCurrency",
            "type": "Element",
        },
    )
    refund_amount_in_home_currency: Optional[Decimal] = (
        field(
            default=None,
            metadata={
                "name": "RefundAmountInHomeCurrency",
                "type": "Element",
            },
        )
    )

@dataclass
class LinkToTxn(QBMixin):
    FIELD_ORDER = [
        "TxnID", "TxnLineID"
    ]

    class Meta:
        name = "LinkToTxn"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )


# endregion


# region Lines


@dataclass
class ExpenseLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "AccountRef", "Amount", "Memo", "CustomerRef",
        "ClassRef", "BillableStatus", "SalesRepRef", "DataExt"
    ]

    class Meta:
        name = "ExpenseLineAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class ExpenseLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "AccountRef", "Amount", "Memo",
        "CustomerRef", "ClassRef", "BillableStatus", "SalesRepRef"
    ]

    class Meta:
        name = "ExpenseLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )


@dataclass
class ExpenseLine(QBMixin):

    class Meta:
        name = "ExpenseLine"

    Add: Type[ExpenseLineAdd] = ExpenseLineAdd
    Mod: Type[ExpenseLineMod] = ExpenseLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "Desc", "Quantity",
        "UnitOfMeasure", "Cost", "Amount", "CustomerRef",
        "ClassRef", "BillableStatus", "OverrideItemAccountRef",
        "LinkToTxn", "SalesRepRef", "DataExt"
    ]

    class Meta:
        name = "ItemLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    link_to_txn: Optional[LinkToTxn] = field(
        default=None,
        metadata={
            "name": "LinkToTxn",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class ItemLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "Desc", "Quantity",
        "UnitOfMeasure", "OverrideUOMSetRef", "Cost", "Amount",
        "CustomerRef", "ClassRef", "BillableStatus", "OverrideItemAccountRef",
        "SalesRepRef"
    ]

    class Meta:
        name = "ItemLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )


@dataclass
class ItemLine(QBMixin):

    class Meta:
        name = "ItemLine"

    Add: Type[ItemLineAdd] = ItemLineAdd
    Mod: Type[ItemLineMod] = ItemLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "ItemGroupLineAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "ItemLineMod"
    ]

    class Meta:
        name = "ItemGroupLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupLine(QBMixin):

    class Meta:
        name = "ItemGroupLine"

    Add: Type[ItemGroupLineAdd] = ItemGroupLineAdd
    Mod: Type[ItemGroupLineMod] = ItemGroupLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    item_lines: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblyLine(QBMixin):

    class Meta:
        name = "ItemInventoryAssemblyLine"

    Add: Type = 'self'
    Mod: Type = 'self'

    item_inventory_ref: Optional[ItemInventoryRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryRef",
            "type": "Element",
            "required": True,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )


@dataclass
class ComponentItemLine(QBMixin):
    class Meta:
        name = "ComponentItemLine"

    Add: Type = 'self'
    Mod: Type = 'self'

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    quantity_needed: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityNeeded",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "Rate", "RatePercent",
        "PriceLevelRef", "ClassRef", "Amount", "InventorySiteRef",
        "InventorySiteLocationRef", "SerialNumber", "LotNumber", "ServiceDate",
        "SalesTaxCodeRef", "OverrideItemAccountRef", "Other1", "Other2",
        "CreditCardTxnInfo", "DataExt"
    ]

    class Meta:
        name = "CreditMemoLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "Rate", "RatePercent", "PriceLevelRef",
        "ClassRef", "Amount", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "ServiceDate", "SalesTaxCodeRef",
        "OverrideItemAccountRef", "Other1", "Other2"
    ]

    class Meta:
        name = "CreditMemoLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[bool] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class CreditMemoLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "ClassRef", "Amount", "InventorySiteRef",
        "InventorySiteLocationRef", "SerialNumber", "LotNumber", "ServiceDate",
        "SalesTaxCodeRef", "Other1", "Other2", "CreditCardTxnInfo", "DataExtRet"
    ]

    class Meta:
        name = "CreditMemoLine"

    Add: Type[CreditMemoLineAdd] = CreditMemoLineAdd
    Mod: Type[CreditMemoLineMod] = CreditMemoLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoLineGroupAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "CreditMemoLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "CreditMemoLineMod"
    ]

    class Meta:
        name = "CreditMemoLineGroupMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    credit_memo_line_mod: List[CreditMemoLineMod] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineMod",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "IsPrintItemsInGroup", "TotalAmount", "CreditMemoLineRet", "CreditCardTxnInfo",
        "DataExtRet"
    ]

    Add: Type[CreditMemoLineGroupAdd] = CreditMemoLineGroupAdd
    Mod: Type[CreditMemoLineGroupMod] = CreditMemoLineGroupMod

    class Meta:
        name = "CreditMemoLineGroup"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[float] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    credit_memo_lines: List[CreditMemoLine] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class DepositLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "PaymentTxnID", "PaymentTxnLineID", "OverrideMemo", "OverrideCheckNumber",
        "OverrideClassRef", "EntityRef", "AccountRef", "Memo", "CheckNumber",
        "PaymentMethodRef", "ClassRef", "Amount"
    ]

    class Meta:
        name = "DepositLineAdd"

    payment_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnID",
            "type": "Element",
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
            "type": "Element",
        },
    )
    override_memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideMemo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    override_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideCheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    override_class_ref: Optional[OverrideClassRef] = field(
        default=None,
        metadata={
            "name": "OverrideClassRef",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class DepositLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "PaymentTxnID", "PaymentTxnLineID", "OverrideMemo",
        "OverrideCheckNumber", "OverrideClassRef", "EntityRef", "AccountRef",
        "Memo", "CheckNumber", "PaymentMethodRef", "ClassRef", "Amount"
    ]

    class Meta:
        name = "DepositLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    payment_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnID",
            "type": "Element",
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
            "type": "Element",
        },
    )
    override_memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideMemo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    override_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideCheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    override_class_ref: Optional[OverrideClassRef] = field(
        default=None,
        metadata={
            "name": "OverrideClassRef",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class DepositLine(QBMixin):
    class Meta:
        name = "DepositLine"

    Add: Type[DepositLineAdd] = DepositLineAdd
    Mod: Type[DepositLineMod] = DepositLineMod

    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "valid_values": VALID_TXN_TYPE_VALUES
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class EstimateLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "Rate", "RatePercent",
        "ClassRef", "Amount", "OptionForPriceRuleConflict", "InventorySiteRef",
        "InventorySiteLocationRef", "SalesTaxCodeRef", "MarkupRate",
        "MarkupRatePercent", "PriceLevelRef", "OverrideItemAccountRef", "Other1",
        "Other2", "DataExt"
    ]

    class Meta:
        name = "EstimateLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    markup_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "MarkupRate",
            "type": "Element",
        },
    )
    markup_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "MarkupRatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )

@dataclass
class EstimateLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "ClassRef", "Amount", "OptionForPriceRuleConflict",
        "InventorySiteRef", "InventorySiteLocationRef", "SalesTaxCodeRef",
        "MarkupRate", "MarkupRatePercent", "PriceLevelRef", "Other1", "Other2"
    ]

    class Meta:
        name = "EstimateLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    markup_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "MarkupRate",
            "type": "Element",
        },
    )
    markup_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "MarkupRatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class EstimateLine(QBMixin):
    class Meta:
        name = "EstimateLine"

    Add: Type[EstimateLineAdd] = EstimateLineAdd
    Mod: Type[EstimateLineMod] = EstimateLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    markup_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "MarkupRate",
            "type": "Element",
        },
    )
    markup_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "MarkupRatePercent",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class EstimateLineGroupAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "EstimateLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class EstimateLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "EstimateLineMod"
    ]

    class Meta:
        name = "NameFilter"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    estimate_line_mod: List[EstimateLineMod] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineMod",
            "type": "Element",
        },
    )


@dataclass
class EstimateLineGroup(QBMixin):
    class Meta:
        name = "EstimateLineGroup"

    Add: Type[EstimateLineGroupAdd] = EstimateLineGroupAdd
    Mod: Type[EstimateLineGroupMod] = EstimateLineGroupMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    estimate_lines: List[EstimateLine] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SerialNumberAdjustment(QBMixin):

    class Meta:
        name = "SerialNumberAdjustment"

    Add: Type = 'self'
    Mod: Type = 'self'

    add_serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AddSerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    remove_serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RemoveSerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )


@dataclass
class LotNumberAdjustment(QBMixin):

    class Meta:
        name = "LotNumberAdjustment"

    Add: Type = 'self'
    Mod: Type = 'self'

    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    count_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "CountAdjustment",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentLineAdd(QBAddMixin):

    class Meta:
        name = "InventoryAdjustmentLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    quantity_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityAdjustment",
            "type": "Element",
        },
    )
    value_adjustment: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueAdjustment",
            "type": "Element",
        },
    )
    serial_number_adjustment: Optional[SerialNumberAdjustment] = field(
        default=None,
        metadata={
            "name": "SerialNumberAdjustment",
            "type": "Element",
        },
    )
    lot_number_adjustment: Optional[LotNumberAdjustment] = field(
        default=None,
        metadata={
            "name": "LotNumberAdjustment",
            "type": "Element",
        },
    )

@dataclass
class InventoryAdjustmentLineMod(QBModMixin):
    class Meta:
        name = "InventoryAdjustmentLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    count_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "CountAdjustment",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity_difference: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityDifference",
            "type": "Element",
        },
    )
    value_difference: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueDifference",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "SerialNumber", "SerialNumberAddedOrRemoved",
        "LotNumber", "InventorySiteLocationRef", "QuantityDifference", "ValueDifference"
    ]

    Add: Type[InventoryAdjustmentLineAdd] = InventoryAdjustmentLineAdd
    Mod: Type[InventoryAdjustmentLineMod] = InventoryAdjustmentLineMod

    class Meta:
        name = "NameFilter"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    serial_number_added_or_removed: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "SerialNumberAddedOrRemoved",
                "type": "Element",
                "valid_values": ["Added", "Removed"],
            },
        )
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity_difference: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityDifference",
            "type": "Element",
            "required": True,
        },
    )
    value_difference: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueDifference",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class InvoiceLineAdd(QBAddMixin):

    FIELD_ORDER = [
        "item_ref", "desc", "quantity", "unit_of_measure", "rate", "rate_percent",
        "price_level_ref", "class_ref", "amount", "option_for_price_rule_conflict",
        "inventory_site_ref", "inventory_site_location_ref", "serial_number",
        "lot_number", "service_date", "sales_tax_code_ref", "override_item_account_ref",
        "other1", "other2", "link_to_txn", "data_ext"
    ]

    class Meta:
        name = "InvoiceLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    link_to_txn: Optional[LinkToTxn] = field(
        default=None,
        metadata={
            "name": "LinkToTxn",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class InvoiceLineMod(QBModMixin):

    class Meta:
        name = "InvoiceLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class InvoiceLine(QBMixin):

    class Meta:
        name = "InvoiceLine"

    Add: Type[InvoiceLineAdd] = InvoiceLineAdd
    Mod: Type[InvoiceLineMod] = InvoiceLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class InvoiceLineGroupAdd(QBAddMixin):

    FIELD_ORDER = [
        "item_group_ref", "quantity", "unit_of_measure", "inventory_site_ref",
        "inventory_site_location_ref", "data_ext"
    ]

    class Meta:
        name = "InvoiceLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    # data_ext: List[DataExt] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExt",
    #         "type": "Element",
    #     },
    # )


@dataclass
class InvoiceLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "InvoiceLineMod"
    ]

    class Meta:
        name = "InvoiceLineGroupMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    invoice_line_mod: List[InvoiceLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineMod",
            "type": "Element",
        },
    )


@dataclass
class InvoiceLineGroup(QBMixin):

    class Meta:
        name = "InvoiceLineGroup"

    Add: Type[InvoiceLineGroupAdd] = InvoiceLineGroupAdd
    Mod: Type[InvoiceLineGroupMod] = InvoiceLineGroupMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    invoice_lines: List[InvoiceLine] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class JournalLineMod(QBModMixin):
    class Meta:
        name = "JournalLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    journal_line_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "JournalLineType",
            "type": "Element",
            "valid_values": {
                "JournalLineType": ["Debit", "Credit"],
            }

        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )


@dataclass
class JournalDebitLine(QBMixin):
    FIELD_ORDER = ["TxnLineID", "AccountRef", "Amount", "Memo", "EntityRef",
                   "ClassRef", "BillableStatus"]

    # Add is a special case here because it's only one of 2 classes that actually references itself.
    Add: Type = "self"
    Mod: Type[JournalLineMod] = JournalLineMod

    class Meta:
        name = "JournalDebitLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class JournalCreditLine(QBMixin):
    FIELD_ORDER = ["TxnLineID", "AccountRef", "Amount", "Memo", "EntityRef",
                   "ClassRef", "BillableStatus"]

    # Add is a special case here because it's only one of 2 classes that actually references itself.
    Add: Type = 'self'
    Mod: Type[JournalLineMod] = JournalLineMod

    class Meta:
        name = "JournalCreditLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class PurchaseOrderLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "ManufacturerPartNumber", "Desc", "Quantity", "UnitOfMeasure",
        "Rate", "ClassRef", "Amount", "InventorySiteLocationRef", "CustomerRef",
        "ServiceDate", "OverrideItemAccountRef", "Other1", "Other2", "DataExt"
    ]

    class Meta:
        name = "PurchaseOrderLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class PurchaseOrderLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "ManufacturerPartNumber", "Desc", "Quantity",
        "UnitOfMeasure", "OverrideUOMSetRef", "Rate", "ClassRef", "Amount",
        "InventorySiteLocationRef", "CustomerRef", "ServiceDate",
        "IsManuallyClosed", "OverrideItemAccountRef", "Other1", "Other2"
    ]

    class Meta:
        name = "PurchaseOrderLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class PurchaseOrderLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "ManufacturerPartNumber", "Desc",
        "Quantity", "UnitOfMeasure", "OverrideUOMSetRef", "Rate",
        "ClassRef", "Amount", "InventorySiteLocationRef", "CustomerRef",
        "ServiceDate", "ReceivedQuantity", "UnbilledQuantity", "IsBilled",
        "IsManuallyClosed", "Other1", "Other2", "DataExtRet"
    ]

    class Meta:
        name = "PurchaseOrderLine"

    Add: Type[PurchaseOrderLineAdd] = PurchaseOrderLineAdd
    Mod: Type[PurchaseOrderLineMod] = PurchaseOrderLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    received_quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "ReceivedQuantity",
            "type": "Element",
        },
    )
    unbilled_quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "UnbilledQuantity",
            "type": "Element",
        },
    )
    is_billed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsBilled",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLineGroupAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "PurchaseOrderLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "PurchaseOrderLineMod"
    ]

    class Meta:
        name = "PurchaseOrderLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    purchase_order_line_mod: List[PurchaseOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineMod",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "IsPrintItemsInGroup", "TotalAmount",
        "PurchaseOrderLineRet", "DataExtRet"
    ]

    Add: Type[PurchaseOrderLineGroupAdd] = PurchaseOrderLineGroupAdd
    Mod: Type[PurchaseOrderLineGroupMod] = PurchaseOrderLineGroupMod

    class Meta:
        name = "PurchaseOrderLineGroup"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    purchase_order_lines: List[PurchaseOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "Rate", "RatePercent",
        "PriceLevelRef", "ClassRef", "Amount", "OptionForPriceRuleConflict",
        "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber", "LotNumber",
        "SalesTaxCodeRef", "IsManuallyClosed", "Other1", "Other2", "DataExt"
    ]

    class Meta:
        name = "SalesOrderLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "PriceLevelRef", "ClassRef", "Amount",
        "OptionForPriceRuleConflict", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "SalesTaxCodeRef", "IsManuallyClosed", "Other1", "Other2"
    ]

    class Meta:
        name = "SalesOrderLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class SalesOrderLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "ClassRef", "Amount", "InventorySiteRef",
        "InventorySiteLocationRef", "SerialNumber", "LotNumber", "SalesTaxCodeRef",
        "Invoiced", "IsManuallyClosed", "Other1", "Other2", "DataExtRet"
    ]

    class Meta:
        name = "SalesOrderLine"

    Add: Type[SalesOrderLineAdd] = SalesOrderLineAdd
    Mod: Type[SalesOrderLineMod] = SalesOrderLineMod

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    invoiced: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Invoiced",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderLineGroupAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "SalesOrderLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "SalesOrderLineMod"
    ]

    class Meta:
        name = "SalesOrderLineGroupMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    sales_order_line_mod: List[SalesOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineMod",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "IsPrintItemsInGroup", "TotalAmount", "SalesOrderLineRet",
        "DataExtRet"
    ]

    Add: Type[SalesOrderLineGroupAdd] = SalesOrderLineGroupAdd
    Mod: Type[SalesOrderLineGroupMod] = SalesOrderLineGroupMod

    class Meta:
        name = "SalesOrderLineGroup"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    sales_order_lines: List[SalesOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLineAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "Rate", "RatePercent",
        "PriceLevelRef", "ClassRef", "Amount", "OptionForPriceRuleConflict",
        "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "ServiceDate", "SalesTaxCodeRef", "OverrideItemAccountRef",
        "Other1", "Other2", "CreditCardTxnInfo", "DataExt"
    ]

    class Meta:
        name = "SalesReceiptLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class SalesReceiptLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "PriceLevelRef", "ClassRef", "Amount",
        "OptionForPriceRuleConflict", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "ServiceDate", "SalesTaxCodeRef",
        "OverrideItemAccountRef", "Other1", "Other2"
    ]

    class Meta:
        name = "SalesReceiptLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class SalesReceiptLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "ClassRef", "Amount", "InventorySiteRef",
        "InventorySiteLocationRef", "SerialNumber", "LotNumber", "ServiceDate",
        "SalesTaxCodeRef", "Other1", "Other2", "CreditCardTxnInfo", "DataExtRet"
    ]

    Add: Type[SalesReceiptLineAdd] = SalesReceiptLineAdd
    Mod: Type[SalesReceiptLineMod] = SalesReceiptLineMod

    class Meta:
        name = "SalesReceiptLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLineGroupAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "SalesReceiptLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLineGroupMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "SalesReceiptLineMod"
    ]

    class Meta:
        name = "SalesReceiptLineGroupMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    sales_receipt_line_mod: List[SalesReceiptLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineMod",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "IsPrintItemsInGroup", "TotalAmount",
        "SalesReceiptLineRet", "DataExtRet"
    ]

    Add: Type[SalesReceiptLineGroupAdd] = SalesReceiptLineGroupAdd
    Mod: Type[SalesReceiptLineGroupMod] = SalesReceiptLineGroupMod

    class Meta:
        name = "SalesReceiptLineGroup"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_receipt_lines: List[SalesReceiptLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

# endregion


# region Lists


@dataclass
class TaxLineInfo(QBMixin):
    class Meta:
        name = "TaxLineInfo"

    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
            "type": "Element",
            "required": True,
        },
    )
    tax_line_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineName",
            "type": "Element",
            "max_length": 256,
        },
    )


@dataclass
class AccountBase:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountType",
            "type": "Element",
            "valid_values": VALID_ACCOUNT_TYPE_VALUES,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 7,
        },
    )
    bank_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "BankNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 200,
        },
    )
    open_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenBalance",
            "type": "Element",
        },
    )
    open_balance_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OpenBalanceDate",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class AccountQuery(QBQueryMixin):
    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "account_type", "currency_filter",
        "include_ret_element", "owner_id",
    ]

    class Meta:
        name = "AccountQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    # request_id: Optional[str] = field(
    #     default="0",
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )


@dataclass
class AccountAdd(AccountBase, QBAddRqMixin):
    FIELD_ORDER = [
        "name", "is_active", "parent_ref", "account_type", "account_number",
        "bank_number", "desc", "open_balance", "open_balance_date",
        "tax_line_id", "currency_ref", "include_ret_element"
    ]

    class Meta:
        name = "AccountAdd"

    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
            "type": "Element",
        },
    )


@dataclass
class SpecialAccountAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "SpecialAccountType", "CurrencyRef"
    ]

    class Meta:
        name = "SpecialAccountAdd"

    special_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialAccountType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "AccountsPayable", "AccountsReceivable", "CondenseItemAdjustmentExpenses",
                "CostOfGoodsSold", "DirectDepositLiabilities", "Estimates",
                "ExchangeGainLoss", "InventoryAssets", "ItemReceiptAccount",
                "OpeningBalanceEquity", "PayrollExpenses", "PayrollLiabilities",
                "PettyCash", "PurchaseOrders", "ReconciliationDifferences",
                "RetainedEarnings", "SalesOrders", "SalesTaxPayable",
                "UncategorizedExpenses", "UncategorizedIncome", "UndepositedFunds"
            ],
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class AccountMod(AccountBase, QBModRqMixin):
    FIELD_ORDER = [
        "list_id", "edit_sequence", "name", "is_active", "parent_ref",
        "account_type", "account_number", "bank_number", "desc",
        "open_balance", "open_balance_date", "tax_line_id",
        "currency_ref", "include_ret_element"
    ]

    class Meta:
        name = "AccountMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
            
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class Account(AccountBase, QBMixinWithSave):
    class Meta:
        name = "Account"
        plural_class_name = "Accounts"

    Query: Type[AccountQuery] = AccountQuery
    Add: Type[AccountAdd] = AccountAdd
    SpecialAccountAdd: Type[SpecialAccountAdd] = SpecialAccountAdd
    Mod: Type[AccountMod] = AccountMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    full_name: Optional[str] = field(default=None, metadata={**full_name.metadata, "max_length": 159})
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    detail_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailAccountType",
            "type": "Element",
            "valid_values": VALID_DETAIL_ACCOUNT_TYPE_VALUES,
        },
    )
    special_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialAccountType",
            "type": "Element",
            "valid_values": VALID_SPECIAL_ACCOUNT_TYPE_VALUES,
        },
    )
    is_tax_account: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxAccount",
            "type": "Element",
        },
    )
    last_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastCheckNumber",
            "type": "Element",
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Balance",
            "type": "Element",
        },
    )
    total_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalBalance",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    tax_line_info_ret: List[TaxLineInfo] = field(
        default_factory=list,
        metadata={
            "name": "TaxLineInfoRet",
            "type": "Element",
        },
    )
    cash_flow_classification: Optional[str] = field(
        default=None,
        metadata={
            "name": "CashFlowClassification",
            "type": "Element",
            "valid_values": VALID_CASH_FLOW_CLASSIFICATION_VALUES,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )

    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Accounts(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Account"
        plural_of = Account

    def __init__(self):
        super().__init__()

    # endregion


@dataclass
class BillingRatePerItem(QBMixin):
    FIELD_ORDER = [
        "ItemRef", "CustomRate", "CustomRatePercent", "AdjustPercentage",
        "AdjustBillingRateRelativeTo"
    ]

    class Meta:
        name = "BillingRatePerItem"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomRate",
            "type": "Element",
        },
    )
    custom_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "CustomRatePercent",
            "type": "Element",
        },
    )
    adjust_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "AdjustPercentage",
            "type": "Element",
        },
    )
    adjust_billing_rate_relative_to: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "AdjustBillingRateRelativeTo",
                "type": "Element",
                "valid_value": ["StandardRate", "CurrentCustomRate"]
            },
        )
    )

@dataclass
class BillingRateQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "FromModifiedDate", "ToModifiedDate",
        "NameFilter", "NameRangeFilter", "ItemRef", "IncludeRetElement"
    ]

    class Meta:
        name = "BillingRateQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class BillingRateAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "FixedBillingRate", "BillingRatePerItem"
    ]

    class Meta:
        name = "BillingRateAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    fixed_billing_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FixedBillingRate",
            "type": "Element",
        },
    )
    billing_rate_per_item: List[BillingRatePerItem] = field(
        default_factory=list,
        metadata={
            "name": "BillingRatePerItem",
            "type": "Element",
        },
    )


@dataclass
class BillingRate(QBMixin):
    class Meta:
        name = "BillingRate"
        plural_class_name = "BillingRates"

    Query: Type[BillingRateQuery] = BillingRateQuery
    Add: Type[BillingRateAdd] = BillingRateAdd
    # there is no Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    billing_rate_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillingRateType",
            "type": "Element",
            "valid_values": ["FixedRate", "PerItem"]
        },
    )
    fixed_billing_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FixedBillingRate",
            "type": "Element",
        },
    )
    billing_rate_per_item_ret: List[BillingRatePerItem] = field(
        default_factory=list,
        metadata={
            "name": "BillingRatePerItemRet",
            "type": "Element",
        },
    )


@dataclass
class BillingRates(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "BillingRate"
        plural_of = BillingRate

    def __init__(self):
        super().__init__()


@dataclass
class ClassInQBQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "ClassQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default="All",
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class ClassInQBAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "ClassAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )


@dataclass
class ClassInQBMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "ClassMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )


@dataclass
class ClassInQB(QBMixinWithSave):
    class Meta:
        name = "Class"
        plural_class_name = "ClassesInQB"

    Query: Type[ClassInQBQuery] = ClassInQBQuery
    Add: Type[ClassInQBAdd] = ClassInQBAdd
    Mod: Type[ClassInQBMod] = ClassInQBMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element"
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element"
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31
        },
    )
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element"
        },
    )
    parent_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element"
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element"
        },
    )


@dataclass
class ClassesInQB(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Class"
        plural_of = ClassInQB

    def __init__(self):
        super().__init__()


@dataclass
class CurrencyFormat(QBMixin):
    thousand_separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThousandSeparator",
            "type": "Element",
            "valid_values": ["Comma", "Period", "Space", "Apostrophe"]
        },
    )
    thousand_separator_grouping: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThousandSeparatorGrouping",
            "type": "Element",
            "valid_values": ["Comma", "Period", "Space", "Apostrophe"]
        },
    )
    decimal_places: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalPlaces",
            "type": "Element",
            "valid_values": ["0", "2"]
        },
    )
    decimal_separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalSeparator",
            "type": "Element",
            "valid_values": ["Period", "Comma"]
        },
    )


@dataclass
class CurrencyQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "CurrencyQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: CurrencyQueryRqTypeMetaData = field(
    #     default=CurrencyQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )


@dataclass
class CurrencyAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "CurrencyCode", "CurrencyFormat", "IncludeRetElement"
    ]

    class Meta:
        name = "CurrencyAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "required": True,
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )


@dataclass
class CurrencyMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "CurrencyCode",
        "CurrencyFormat"
    ]

    class Meta:
        name = "CurrencyMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )


@dataclass
class Currency(QBMixinWithSave):
    class Meta:
        name = "Currency"
        plural_class_name = "Currencies"

    Query: Type[CurrencyQuery] = CurrencyQuery
    Add: Type[CurrencyAdd] = CurrencyAdd
    Mod: Type[CurrencyMod] = CurrencyMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )
    is_user_defined_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsUserDefinedCurrency",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    as_of_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AsOfDate",
            "type": "Element",
        },
    )


@dataclass
class Currencies(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Currency"
        plural_of = Currency

    def __init__(self):
        super().__init__()


@dataclass
class CustomerMsgQuery(QBQueryMixin):

    class Meta:
        name = "CustomerMsgQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"]
    #     },
    # )


@dataclass
class CustomerMsgAdd(QBAddRqMixin):

    class Meta:
        name = "CustomerMsgAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 101,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class CustomerMsg(QBMixinWithSave):

    class Meta:
        name = "CustomerMsg"
        plural_class_name = "CustomerMsgs"

    Query: Type[CustomerMsgQuery] = CustomerMsgQuery
    Add: Type[CustomerMsgAdd] = CustomerMsgAdd
    #There is no Mod


    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 101,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class CustomerMsgs(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "CustomerMsg"
        plural_of = CustomerMsg

    def __init__(self):
        super().__init__()


@dataclass
class CustomerQuery(QBQueryMixin):

    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "total_balance_filter", "currency_filter",
        "class_filter", "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "CustomerQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    total_balance_filter: Optional[TotalBalanceFilter] = field(
        default=None,
        metadata={
            "name": "TotalBalanceFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class CustomerAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ClassRef", "ParentRef", "CompanyName", "Salutation",
        "FirstName", "MiddleName", "LastName", "JobTitle", "BillAddress",
        "ShipAddress", "ShipToAddress", "Phone", "AltPhone", "Fax", "Email", "Cc",
        "Contact", "AltContact", "AdditionalContactRef", "Contacts",
        "CustomerTypeRef", "TermsRef", "SalesRepRef", "OpenBalance",
        "OpenBalanceDate", "SalesTaxCodeRef", "ItemSalesTaxRef", "ResaleNumber",
        "AccountNumber", "CreditLimit", "PreferredPaymentMethodRef",
        "CreditCardInfo", "JobStatus", "JobStartDate", "JobProjectedEndDate",
        "JobEndDate", "JobDesc", "JobTypeRef", "Notes", "AdditionalNotes",
        "PreferredDeliveryMethod", "PriceLevelRef", "ExternalGUID", "CurrencyRef"
    ]

    class Meta:
        name = "CustomerAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element",
        },
    )
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    open_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenBalance",
            "type": "Element",
        },
    )
    open_balance_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OpenBalanceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_country: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesTaxCountry",
            "type": "Element",
            "valid_values": ["Australia", "Canada", "UK", "US"]
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element",
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element",
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element",
            "valid_values": ["Awarded", "Closed", "InProgress", "None", "NotAwarded", "Pending"]
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element",
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element",
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element",
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99,
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    additional_notes: List[AdditionalNotes] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotes",
            "type": "Element",
        },
    )
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )

@dataclass
class CustomerMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ClassRef", "ParentRef",
        "CompanyName", "Salutation", "FirstName", "MiddleName", "LastName",
        "JobTitle", "BillAddress", "ShipAddress", "ShipToAddress", "Phone",
        "AltPhone", "Fax", "Email", "Cc", "Contact", "AltContact",
        "AdditionalContactRef", "ContactsMod", "CustomerTypeRef", "TermsRef",
        "SalesRepRef", "SalesTaxCodeRef", "ItemSalesTaxRef", "ResaleNumber",
        "AccountNumber", "CreditLimit", "PreferredPaymentMethodRef",
        "CreditCardInfo", "JobStatus", "JobStartDate", "JobProjectedEndDate",
        "JobEndDate", "JobDesc", "JobTypeRef", "Notes", "AdditionalNotesMod",
        "PreferredDeliveryMethod", "PriceLevelRef", "CurrencyRef"
    ]

    class Meta:
        name = "CustomerMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts_mod: List[ContactsMod] = field(
        default_factory=list,
        metadata={
            "name": "ContactsMod",
            "type": "Element",
        },
    )
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element",
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element",
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element",
            "valid_values": ["Awarded", "Closed", "InProgress", "None", "NotAwarded", "Pending"]
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element",
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element",
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element",
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99,
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    additional_notes_mod: List[AdditionalNotesMod] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesMod",
            "type": "Element",
        },
    )
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class Customer(QBMixinWithSave):
    class Meta:
        name = "Customer"
        plural_class_name = "Customers"

    Query: Type[CustomerQuery] = CustomerQuery
    Add: Type[CustomerAdd] = CustomerAdd
    Mod: Type[CustomerMod] = CustomerMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element"
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element"
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41
        },
    )
    full_name: Optional[str] = full_name
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element"
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element"
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element"
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element"
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element"
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8
        },
    )
    contacts_ret: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element"
        },
    )
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
            "type": "Element"
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element"
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element"
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Balance",
            "type": "Element"
        },
    )
    total_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalBalance",
            "type": "Element"
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element"
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element"
        },
    )
    sales_tax_country: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesTaxCountry",
            "type": "Element",
            "valid_values": ["Australia", "Canada", "UK", "US"]
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99
        },
    )
    credit_limit: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element"
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element"
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element"
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element"
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element"
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element"
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element"
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element"
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095
        },
    )
    additional_notes_ret: List[AdditionalNotesRet] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesRet",
            "type": "Element"
        },
    )
    is_statement_with_parent: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsStatementWithParent",
            "type": "Element"
        },
    )
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element"
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element"
        },
    )
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element"
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element"
        },
    )


@dataclass
class Customers(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "Customer"
        plural_of = Customer

    def __init__(self):
        super().__init__()


@dataclass
class EmergencyContact(QBMixin):
    # this class is meant to be inherited
    class Meta:
        name = ""

    contact_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactName",
            "type": "Element",
            "required": True,
            "max_length": 40,
        },
    )
    contact_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactValue",
            "type": "Element",
            "required": True,
            "max_length": 255,
        },
    )
    relation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Relation",
            "type": "Element",
            "valid_values": VALID_RELATION_VALUES
        },
    )


@dataclass
class PrimaryContact(EmergencyContact):
    class Meta:
        name = "PrimaryContact"


@dataclass
class SecondaryContact(EmergencyContact):
    class Meta:
        name = "SecondaryContact"


@dataclass
class EmergencyContacts(QBMixin):
    class Meta:
        name = "EmergencyContacts"

    primary_contact: Optional[PrimaryContact] = field(
        default=None,
        metadata={
            "name": "PrimaryContact",
            "type": "Element",
        },
    )
    secondary_contact: Optional[SecondaryContact] = field(
        default=None,
        metadata={
            "name": "SecondaryContact",
            "type": "Element",
        },
    )


@dataclass
class Earnings(QBMixin):
    class Meta:
        name = "Earnings"

    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
            "type": "Element",
            "required": True,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )


@dataclass
class AccruedHours(QBMixin):
    #this class is meant to be inherited
    class Meta:
        name = ""

    hours_available: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursAvailable",
            "type": "Element",
        },
    )
    accrual_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccrualPeriod",
            "type": "Element",
            "valid_values": ["BeginningOfYear", "EveryHourOnPaycheck", "EveryPaycheck"]
        },
    )
    hours_accrued: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursAccrued",
            "type": "Element",
        },
    )
    maximum_hours: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "MaximumHours",
            "type": "Element",
        },
    )
    is_resetting_hours_each_new_year: Optional[bool] = (
        field(
            default=None,
            metadata={
                "name": "IsResettingHoursEachNewYear",
                "type": "Element",
            },
        )
    )
    hours_used: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursUsed",
            "type": "Element",
        },
    )
    accrual_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AccrualStartDate",
            "type": "Element",
        },
    )


@dataclass
class SickHours(AccruedHours):
    #this class is meant to be inherited
    class Meta:
        name = "SickHours"

    employee_payroll_info_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "EmployeePayrollInfoId",
            "type": "Element",
        },
    )


@dataclass
class VacationHours(AccruedHours):
    #this class is meant to be inherited
    class Meta:
        name = "VacationHours"

    employee_payroll_info_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "EmployeePayrollInfoId",
            "type": "Element",
        },
    )


@dataclass
class EmployeePayrollInfo(QBMixin):

    class Meta:
        name = "EmployeePayrollInfo"

    pay_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "PayPeriod",
            "type": "Element",
            "valid_values": ["Daily", "Weekly", "Biweekly", "Semimonthly", "Monthly", "Quarterly", "Yearly"]
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    clear_earnings: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearEarnings",
            "type": "Element",
        },
    )
    earnings: List[Earnings] = field(
        default_factory=list,
        metadata={
            "name": "Earnings",
            "type": "Element",
        },
    )
    use_time_data_to_create_paychecks: Optional[str] = field(
        default=None,
        metadata={
            "name": "UseTimeDataToCreatePaychecks",
            "type": "Element",
            "valid_values": ["NotSet", "UseTimeData", "DoNotUseTimeData"]
        },
    )
    sick_hours: Optional[SickHours] = field(
        default=None,
        metadata={
            "name": "SickHours",
            "type": "Element",
        },
    )
    vacation_hours: Optional[VacationHours] = field(
        default=None,
        metadata={
            "name": "VacationHours",
            "type": "Element",
        },
    )


@dataclass
class EmployeeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "EmployeeQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class Employee(QBMixinWithSave):
    class Meta:
        name = "Employee"
        plural_class_name = "Employees"

    class Query(EmployeeQuery):
        pass


    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    supervisor_ref: Optional[SupervisorRef] = field(
        default=None,
        metadata={
            "name": "SupervisorRef",
            "type": "Element",
        },
    )
    department: Optional[str] = field(
        default=None,
        metadata={
            "name": "Department",
            "type": "Element",
            "max_length": 31,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "max_length": 64,
        },
    )
    target_bonus: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TargetBonus",
            "type": "Element",
        },
    )
    employee_address: Optional[EmployeeAddress] = field(
        default=None,
        metadata={
            "name": "EmployeeAddress",
            "type": "Element",
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager_pin: Optional[str] = field(
        default=None,
        metadata={
            "name": "PagerPIN",
            "type": "Element",
            "max_length": 10,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    ssn: Optional[str] = field(
        default=None,
        metadata={
            "name": "SSN",
            "type": "Element",
            "max_length": 11,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    # additional_contact_ref: List[AdditionalContactRef] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "AdditionalContactRef",
    #         "type": "Element",
    #         "max_occurs": 8,
    #     },
    # )
    emergency_contacts: Optional[EmergencyContacts] = field(
        default=None,
        metadata={
            "name": "EmergencyContacts",
            "type": "Element",
        },
    )
    employee_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "EmployeeType",
            "type": "Element",
        },
    )
    part_or_full_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartOrFullTime",
            "type": "Element",
        },
    )
    exempt: Optional[str] = field(
        default=None,
        metadata={
            "name": "Exempt",
            "type": "Element",
        },
    )
    key_employee: Optional[bool] = field(
        default=None,
        metadata={
            "name": "KeyEmployee",
            "type": "Element",
        },
    )
    gender: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
        },
    )
    hired_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "HiredDate",
            "type": "Element",
        },
    )
    original_hire_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OriginalHireDate",
            "type": "Element",
        },
    )
    adjusted_service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AdjustedServiceDate",
            "type": "Element",
        },
    )
    released_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ReleasedDate",
            "type": "Element",
        },
    )
    birth_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
        },
    )
    us_citizen: Optional[bool] = field(
        default=None,
        metadata={
            "name": "USCitizen",
            "type": "Element",
        },
    )
    ethnicity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ethnicity",
            "type": "Element",
        },
    )
    disabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Disabled",
            "type": "Element",
        },
    )
    disability_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "DisabilityDesc",
            "type": "Element",
            "max_length": 25,
        },
    )
    on_file: Optional[bool] = field(
        default=None,
        metadata={
            "name": "OnFile",
            "type": "Element",
        },
    )
    work_auth_expire_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "WorkAuthExpireDate",
            "type": "Element",
        },
    )
    us_veteran: Optional[bool] = field(
        default=None,
        metadata={
            "name": "USVeteran",
            "type": "Element",
        },
    )
    military_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "MilitaryStatus",
            "type": "Element",
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    # additional_notes_ret: List[AdditionalNotes] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "AdditionalNotesRet",
    #         "type": "Element",
    #     },
    # )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    employee_payroll_info: Optional[EmployeePayrollInfo] = field(
        default=None,
        metadata={
            "name": "EmployeePayrollInfo",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

    IS_YES_NO_FIELD_LIST = ["key_employee", "us_citizen", "disabled", "on_file", "us_veteran"]
    VALID_EMPLOYEE_TYPES = ["Officer", "Owner", "Regular", "Statutory"]
    VALID_PART_OR_FULL_TIME_VALUES = ["PartTime", "FullTime"]
    VALID_EXEMPT_VALUES = ["Exempt", "NonExempt"]
    VALID_GENDER_VALUES = ["Male", "Female"]
    VALID_ETHNICITY_VALUES = ["AmericianIndian", "Asian", "Black", "Hawaiian", "Hispanic", "White", "TwoOrMoreRaces"]
    VALID_MILITARY_STATUS_VALUES = ["Active", "Reserve"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('employee_type', self.employee_type, self.VALID_EMPLOYEE_TYPES)
        self._validate_str_from_list_of_values('part_or_full_time', self.part_or_full_time, self.VALID_PART_OR_FULL_TIME_VALUES)
        self._validate_str_from_list_of_values('exempt', self.exempt, self.VALID_EXEMPT_VALUES)
        self._validate_str_from_list_of_values('gender', self.gender, self.VALID_GENDER_VALUES)
        self._validate_str_from_list_of_values('ethnicity', self.ethnicity, self.VALID_ETHNICITY_VALUES)
        self._validate_str_from_list_of_values('military_status', self.military_status, self.VALID_MILITARY_STATUS_VALUES)


@dataclass
class Employees(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "Employee"
        plural_of = Employee
        # plural_of_db_model = DBEmployee

    def __init__(self):
        super().__init__()


@dataclass
class SiteAddress(AddressBlock):
    class Meta:
        name = "SiteAddress"

    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "max_length": 31
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "max_length": 21
        },
    )
    postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "max_length": 13
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "max_length": 31
        },
    )


@dataclass
class SiteAddressBlock(AddressBlock):
    class Meta:
        name = "SiteAddressBlock"


@dataclass
class InventorySiteQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "ActiveStatus", "FromModifiedDate", "ToModifiedDate",
        "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class InventorySiteAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentSiteRef", "SiteDesc", "Contact", "Phone",
        "Fax", "Email", "SiteAddress", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )


@dataclass
class InventorySiteMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentSiteRef", "SiteDesc",
        "Contact", "Phone", "Fax", "Email", "SiteAddress", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )


@dataclass
class InventorySite(QBMixinWithSave):

    class Meta:
        name = "InventorySite"
        plural_class_name = "InventorySites"

    Query: Type[InventorySiteQuery] = InventorySiteQuery
    Add: Type[InventorySiteAdd] = InventorySiteAdd
    Mod: Type[InventorySiteMod] = InventorySiteMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    is_default_site: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsDefaultSite",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )
    site_address_block: Optional[SiteAddressBlock] = field(
        default=None,
        metadata={
            "name": "SiteAddressBlock",
            "type": "Element",
        },
    )


@dataclass
class InventorySites(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "InventorySite"
        plural_of = InventorySite

    def __init__(self):
        super().__init__()


@dataclass
class BarCode(QBMixin):

    class Meta:
        name = "BarCode"

    bar_code_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "BarCodeValue",
            "type": "Element",
            "max_length": 50,
        },
    )
    assign_even_if_used: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AssignEvenIfUsed",
            "type": "Element",
        },
    )
    allow_override: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AllowOverride",
            "type": "Element",
        },
    )


@dataclass
class SalesAndPurchase(QBMixin):

    class Meta:
        name = "SalesAndPurchase"

    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    expense_account_ref: Optional[ExpenseAccountRef] = field(
        default=None,
        metadata={
            "name": "ExpenseAccountRef",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )


@dataclass
class SalesOrPurchase(QBMixin):

    class Meta:
        name = "SalesOrPurchase"

    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    price: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "Price",
            "type": "Element",
        },
    )
    price_percent: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "PricePercent",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )


@dataclass
class ItemQueryMixin(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter",
        "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = ""

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )

    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class ItemQueryMixinWithClass(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "ClassFilter",
        "IncludeRetElement", "OwnerID"
    ]
    class Meta:
        name = ""

    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscountQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemDiscountQuery"


@dataclass
class ItemGroupQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemGroupQuery"


@dataclass
class ItemInventoryAssemblyQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemInventoryAssemblyQuery"


@dataclass
class ItemInventoryQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemInventoryQuery"


@dataclass
class ItemNonInventoryQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemNonInventoryQuery"


@dataclass
class ItemOtherChargeQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemOtherChargeQuery"


@dataclass
class ItemPaymentQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemPaymentQuery"


@dataclass
class ItemSalesTaxGroupQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemSalesTaxGroupQuery"


@dataclass
class ItemSalesTaxQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemSalesTaxQuery"


@dataclass
class ItemServiceQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemServiceQuery"


@dataclass
class ItemSubtotalQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemSubtotalQuery"


@dataclass
class ItemAddMixin(QBAddRqMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    bar_code: Optional[BarCode] = field(
        default=None,
        metadata={
            "name": "BarCode",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class ItemAddWithClassAndTaxMixin(ItemAddMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscountAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef", "ItemDesc",
        "SalesTaxCodeRef", "DiscountRate", "DiscountRatePercent", "AccountRef",
        "ExternalGUID"
    ]

    class Meta:
        name = "ItemDiscountAdd"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    discount_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "UnitOfMeasureSetRef",
        "IsPrintItemsInGroup", "ExternalGUID", "ItemGroupLine"
    ]

    class Meta:
        name = "ItemDiscountAdd"


    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAddMixin(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = []

    class Meta:
        name = ""

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )

    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    total_value: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalValue",
            "type": "Element",
        },
    )
    inventory_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "InventoryDate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAdd(ItemInventoryAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "ReorderPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID"
    ]

    class Meta:
        name = "ItemInventoryAdd"

    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblyAdd(ItemInventoryAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "BuildPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID", "ItemInventoryAssemblyLine"
    ]

    class Meta:
        name = "ItemInventoryAssemblyAdd"

    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
            "type": "Element",
        },
    )


@dataclass
class ItemNonInventoryAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ParentRef", "ClassRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
    ]
    class Meta:
        name = "ItemNonInventoryAdd"


    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemOtherChargeAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "SalesTaxCodeRef", "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
    ]

    class Meta:
        name = "ItemOtherChargeAdd"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemPaymentAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "DepositToAccountRef", "PaymentMethodRef", "ExternalGUID"
    ]

    class Meta:
        name = "ItemPaymentAdd"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "TaxRate", "TaxVendorRef", "ExternalGUID"
    ]

    class Meta:
        name = "ItemSalesTaxAdd"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxGroupAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID",
        "ItemSalesTaxRef"
    ]

    class Meta:
        name = "ItemSalesTaxGroupAdd"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ItemServiceAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "UnitOfMeasureSetRef", "SalesTaxCodeRef", "SalesOrPurchase",
        "SalesAndPurchase", "ExternalGUID"
    ]

    class Meta:
        name = "ItemServiceAdd"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemSubtotalAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID"
    ]

    class Meta:
        name = "ItemSubtotalAdd"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class ItemModMixin(QBModRqMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    bar_code: Optional[BarCode] = field(
        default=None,
        metadata={
            "name": "BarCode",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class ItemModWithClassAndTaxMixin(ItemModMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscountMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ItemDesc", "SalesTaxCodeRef", "DiscountRate",
        "DiscountRatePercent", "AccountRef", "ApplyAccountRefToExistingTxns"
    ]

    class Meta:
        name = "ItemDiscountMod"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    discount_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    apply_account_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyAccountRefToExistingTxns",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc",
        "UnitOfMeasureSetRef", "ForceUOMChange", "IsPrintItemsInGroup",
        "ClearItemsInGroup", "ItemGroupLine"
    ]

    class Meta:
        name = "ItemDiscountMod"


    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    clear_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemsInGroup",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryModMixin(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = []

    class Meta:
        name = ""

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    apply_income_account_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyIncomeAccountRefToExistingTxns",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
            "type": "Element",
        },
    )
    apply_cogsaccount_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyCOGSAccountRefToExistingTxns",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )

    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryMod(ItemInventoryModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ManufacturerPartNumber", "UnitOfMeasureSetRef",
        "ForceUOMChange", "SalesTaxCodeRef", "SalesDesc", "SalesPrice",
        "IncomeAccountRef", "ApplyIncomeAccountRefToExistingTxns", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "ApplyCOGSAccountRefToExistingTxns",
        "PrefVendorRef", "AssetAccountRef", "ReorderPoint", "Max"
    ]

    class Meta:
        name = "ItemInventoryMod"

    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblyMod(ItemInventoryModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "BuildPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID", "ItemInventoryAssemblyLine"
    ]

    class Meta:
        name = "ItemInventoryAssemblyMod"

    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    clear_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemsInGroup",
            "type": "Element",
        },
    )
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
            "type": "Element",
        },
    )


@dataclass
class ItemNonInventoryMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ManufacturerPartNumber", "UnitOfMeasureSetRef",
        "ForceUOMChange", "SalesTaxCodeRef", "SalesOrPurchaseMod",
        "SalesAndPurchaseMod"
    ]
    class Meta:
        name = "ItemNonInventoryMod"


    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemOtherChargeMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "SalesTaxCodeRef", "SalesOrPurchaseMod",
        "SalesAndPurchaseMod"
    ]

    class Meta:
        name = "ItemOtherChargeMod"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemPaymentMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ItemDesc", "DepositToAccountRef", "PaymentMethodRef"
    ]

    class Meta:
        name = "ItemPaymentMod"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ItemDesc", "TaxRate", "TaxVendorRef"
    ]

    class Meta:
        name = "ItemSalesTaxMod"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxGroupMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc",
        "ItemSalesTaxRef"
    ]

    class Meta:
        name = "ItemSalesTaxGroupMod"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ItemServiceMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "UnitOfMeasureSetRef", "ForceUOMChange", "SalesTaxCodeRef",
        "SalesOrPurchaseMod", "SalesAndPurchaseMod"
    ]

    class Meta:
        name = "ItemServiceMod"

    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )


@dataclass
class ItemSubtotalMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc"
    ]

    class Meta:
        name = "ItemSubtotalMod"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class ItemMixin:
    class Meta:
        name = ""

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    full_name: Optional[str] = field(default=None, metadata={**full_name.metadata, "max_length": 159})
    bar_code_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "BarCodeValue",
            "type": "Element",
            "max_length": 50,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class ItemWithClassAndTaxMixin(ItemMixin):


    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscount(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemDiscount"
        plural_class_name = "ItemDiscounts"

    Query: Type[ItemDiscountQuery] = ItemDiscountQuery
    Add: Type[ItemDiscountAdd] = ItemDiscountAdd
    Mod: Type[ItemDiscountMod] = ItemDiscountMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    discount_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscounts(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemDiscount"
        plural_of = ItemDiscount

    def __init__(self):
        super().__init__()


@dataclass
class ItemGroup(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemGroup"
        plural_class_name = "ItemGroups"

    Query: Type[ItemGroupQuery] = ItemGroupQuery
    Add: Type[ItemGroupAdd] = ItemGroupAdd
    Mod: Type[ItemGroupMod] = ItemGroupMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemGroups(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemGroup"
        plural_of = ItemGroup

    def __init__(self):
        super().__init__()


@dataclass
class ItemInventory(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemInventory"
        plural_class_name = "ItemInventories"

    Query: Type[ItemInventoryQuery] = ItemInventoryQuery
    Add: Type[ItemInventoryAdd] = ItemInventoryAdd
    Mod: Type[ItemInventoryMod] = ItemInventoryMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )
    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )
    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    average_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AverageCost",
            "type": "Element",
        },
    )
    quantity_on_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnOrder",
            "type": "Element",
        },
    )
    quantity_on_sales_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemInventories(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemInventory"
        plural_of = ItemInventory

    def __init__(self):
        super().__init__()


@dataclass
class ItemInventoryAssembly(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemInventoryAssembly"
        plural_class_name = "ItemInventoryAssemblies"

    Query: Type[ItemInventoryAssemblyQuery] = ItemInventoryAssemblyQuery
    Add: Type[ItemInventoryAssemblyAdd] = ItemInventoryAssemblyAdd
    Mod: Type[ItemInventoryAssemblyMod] = ItemInventoryAssemblyMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )
    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    average_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AverageCost",
            "type": "Element",
        },
    )
    quantity_on_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnOrder",
            "type": "Element",
        },
    )
    quantity_on_sales_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblies(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemInventoryAssembly"
        plural_of = ItemInventoryAssembly

    def __init__(self):
        super().__init__()


@dataclass
class ItemNonInventory(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemNonInventory"
        plural_class_name = "ItemInventories"

    Query: Type[ItemNonInventoryQuery] = ItemNonInventoryQuery
    Add: Type[ItemNonInventoryAdd] = ItemNonInventoryAdd
    Mod: Type[ItemNonInventoryMod] = ItemNonInventoryMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemNonInventories(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemNonInventory"
        plural_of = ItemNonInventory

    def __init__(self):
        super().__init__()


@dataclass
class ItemOtherCharge(ItemWithClassAndTaxMixin, QBMixinWithSave):
    class Meta:
        name = "ItemOtherCharge"
        plural_class_name = "ItemOtherCharges"

    Query: Type[ItemOtherChargeQuery] = ItemOtherChargeQuery
    Add: Type[ItemOtherChargeAdd] = ItemOtherChargeAdd
    Mod: Type[ItemOtherChargeMod] = ItemOtherChargeMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemOtherCharges(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemOtherCharge"
        plural_of = ItemOtherCharge

    def __init__(self):
        super().__init__()


@dataclass
class ItemPayment(ItemMixin, QBMixinWithSave):
    class Meta:
        name = "ItemPayment"
        plural_class_name = "ItemPayments"

    Query: Type[ItemPaymentQuery] = ItemPaymentQuery
    Add: Type[ItemPaymentAdd] = ItemPaymentAdd
    Mod: Type[ItemPaymentMod] = ItemPaymentMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemPayments(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemPayment"
        plural_of = ItemPayment

    def __init__(self):
        super().__init__()


@dataclass
class ItemSalesTax(ItemMixin, QBMixinWithSave):
    class Meta:
        name = "ItemSalesTax"
        plural_class_name = "ItemSalesTaxes"

    Query: Type[ItemSalesTaxQuery] = ItemSalesTaxQuery
    Add: Type[ItemSalesTaxAdd] = ItemSalesTaxAdd
    Mod: Type[ItemSalesTaxMod] = ItemSalesTaxMod

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxes(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSalesTax"
        plural_of = ItemSalesTax

    def __init__(self):
        super().__init__()


@dataclass
class ItemSalesTaxGroup(ItemMixin, QBMixinWithSave):
    class Meta:
        name = "ItemSalesTaxGroup"
        plural_class_name = "ItemSalesTaxGroups"

    Query: Type[ItemSalesTaxGroupQuery] = ItemSalesTaxGroupQuery
    Add: Type[ItemSalesTaxGroupAdd] = ItemSalesTaxGroupAdd
    Mod: Type[ItemSalesTaxGroupMod] = ItemSalesTaxGroupMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxGroups(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSalesTaxGroup"
        plural_of = ItemSalesTaxGroup

    def __init__(self):
        super().__init__()


@dataclass
class ItemService(ItemMixin, QBMixinWithSave):
    class Meta:
        name = "ItemService"
        plural_class_name = "ItemServices"

    Query: Type[ItemServiceQuery] = ItemServiceQuery
    Add: Type[ItemServiceAdd] = ItemServiceAdd
    Mod: Type[ItemServiceMod] = ItemServiceMod

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )

    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemServices(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemService"
        plural_of = ItemService

    def __init__(self):
        super().__init__()


@dataclass
class ItemSubtotal(ItemMixin, QBMixinWithSave):
    class Meta:
        name = "ItemSubtotal"
        plural_class_name = "ItemSubtotals"

    Query: Type[ItemSubtotalQuery] = ItemSubtotalQuery
    Add: Type[ItemSubtotalAdd] = ItemSubtotalAdd
    Mod: Type[ItemSubtotalMod] = ItemSubtotalMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
        },
    )
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemSubtotals(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSubtotal"
        plural_of = ItemSubtotal

    def __init__(self):
        super().__init__()


@dataclass
class JobTypeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "JobTypeQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class JobTypeAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "JobTypeAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )


@dataclass
class JobType(QBMixinWithSave):

    class Meta:
        name = "JobType"
        plural_class_name = "JobTypes"

    Query: Type[JobTypeQuery] = JobTypeQuery
    Add: Type[JobTypeAdd] = JobTypeAdd
    #There is no Mod


    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    full_name: Optional[str] = field(default=None, metadata={**full_name.metadata, "max_length": 159})
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )

@dataclass
class JobTypes(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "JobType"
        plural_of = JobType

    def __init__(self):
        super().__init__()


@dataclass
class OtherNameQuery(QBQueryMixin):

    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "OtherNameQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )

    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )

@dataclass
class OtherNameAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "CompanyName", "Salutation", "FirstName",
        "MiddleName", "LastName", "OtherNameAddress", "Phone",
        "AltPhone", "Fax", "Email", "Contact", "AltContact",
        "AccountNumber", "Notes", "ExternalGUID"
    ]

    class Meta:
        name = "OtherNameAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )

@dataclass
class OtherNameMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "CompanyName",
        "Salutation", "FirstName", "MiddleName", "LastName",
        "OtherNameAddress", "Phone", "AltPhone", "Fax", "Email",
        "Contact", "AltContact", "AccountNumber", "Notes"
    ]

    class Meta:
        name = "OtherNameMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class OtherName(QBMixinWithSave):
    class Meta:
        name = "OtherName"
        plural_class_name = "OtherNames"

    Query: Type[OtherNameQuery] = OtherNameQuery
    Add: Type[OtherNameAdd] = OtherNameAdd
    Mod: Type[OtherNameMod] = OtherNameMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
        },
    )
    other_name_address_block: Optional[OtherNameAddressBlock] = field(
        default=None,
        metadata={
            "name": "OtherNameAddressBlock",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class OtherNames(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "OtherName"
        plural_of = OtherName

    def __init__(self):
        super().__init__()


@dataclass
class PaymentMethodQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "PaymentMethodType", "IncludeRetElement"
    ]

    class Meta:
        name = "PaymentMethodQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    payment_method_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class PaymentMethodAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "PaymentMethodType"
    ]

    class Meta:
        name = "PaymentMethodQuery"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    payment_method_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
        },
    )


@dataclass
class PaymentMethod(QBMixinWithSave):
    class Meta:
        name = "PaymentMethod"
        plural_class_name = "PaymentMethods"

    Query: Type[PaymentMethodQuery] = PaymentMethodQuery
    Add: Type[PaymentMethodAdd] = PaymentMethodAdd
    # There is no Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    payment_method_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
        },
    )


@dataclass
class PaymentMethods(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "PaymentMethod"
        plural_of = PaymentMethod

    def __init__(self):
        super().__init__()


@dataclass
class PayrollItemWage(QBMixin):


    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    wage_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "WageType",
            "type": "Element",
        },
    )
    expense_account_ref: Optional[ExpenseAccountRef] = field(
        default=None,
        metadata={
            "name": "ExpenseAccountRef",
            "type": "Element",
        },
    )

    VALID_WAGE_TYPE_VALUES = ["Bonus", "Commission", "HourlyOvertime", "HourlyRegular", "HourlySick",
                              "HourlyVacation", "SalaryRegular", "SalarySick", "SalaryVacation"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('wage_type', self.wage_type, self.VALID_WAGE_TYPE_VALUES)


@dataclass
class PriceLevelPerItem(QBMixin):
    class Meta:
        name = "PriceLevelPerItem"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomPrice",
            "type": "Element",
        },
    )
    custom_price_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "CustomPricePercent",
            "type": "Element",
        },
    )
    adjust_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "AdjustPercentage",
            "type": "Element",
        },
    )
    adjust_relative_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "AdjustRelativeTo",
            "type": "Element",
            "valid_values": ["StandardPrice", "Cost", "CurrentCustomPrice"],
        },
    )


@dataclass
class PriceLevelPerItemRet:
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomPrice",
            "type": "Element",
        },
    )
    custom_price_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "CustomPricePercent",
            "type": "Element",
        },
    )


@dataclass
class PriceLevelQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ItemRef", "CurrencyFilter",
        "IncludeRetElement"
    ]

    class Meta:
        name = "PriceLevelQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )

@dataclass
class PriceLevelAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "PriceLevelFixedPercentage",
        "PriceLevelPerItem", "CurrencyRef"
    ]

    class Meta:
        name = "PriceLevelAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item: List[PriceLevelPerItem] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItem",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class PriceLevelMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive",
        "PriceLevelFixedPercentage", "PriceLevelPerItem",
        "CurrencyRef"
    ]

    class Meta:
        name = "PriceLevelMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item: List[PriceLevelPerItem] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItem",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class PriceLevel(QBMixinWithSave):

    class Meta:
        name = "PriceLevel"
        plural_class_name = "PriceLevels"

    Query: Type[PriceLevelQuery] = PriceLevelQuery
    Add: Type[PriceLevelAdd] = PriceLevelAdd
    Mod: Type[PriceLevelMod] = PriceLevelMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    price_level_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PriceLevelType",
            "type": "Element",
            "valid_values": ["FixedPercentage", "PerItem"]
        },
    )
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item_ret: List[PriceLevelPerItemRet] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItemRet",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class PriceLevels(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "PriceLevel"
        plural_of = PriceLevel

    def __init__(self):
        super().__init__()


@dataclass
class SalesRepQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "SalesRepQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class SalesRepAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Initial", "IsActive", "SalesRepEntityRef"
    ]

    class Meta:
        name = "SalesRepAdd"

    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "required": True,
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SalesRepMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Initial", "IsActive",
        "SalesRepEntityRef"
    ]

    class Meta:
        name = "SalesRepMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
        },
    )


@dataclass
class SalesRep(QBMixinWithSave):

    class Meta:
        name = "SalesRep"
        plural_class_name = "SalesReps"

    Query: Type[SalesRepQuery] = SalesRepQuery
    Add: Type[SalesRepAdd] = SalesRepAdd
    Mod: Type[SalesRepMod] = SalesRepMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
        },
    )


@dataclass
class SalesReps(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "SalesRep"
        plural_of = SalesRep

    def __init__(self):
        super().__init__()


@dataclass
class SalesTaxCodeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "SalesTaxCodeQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class SalesTaxCodeAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "IsTaxable", "Desc"
    ]

    class Meta:
        name = "SalesTaxCodeAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )


@dataclass
class SalesTaxCodeMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive",
        "IsTaxable", "Desc"
    ]

    class Meta:
        name = "SalesTaxCodeMod"

    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )


@dataclass
class SalesTaxCode(QBMixinWithSave):
    class Meta:
        name = "SalesTaxCode"
        plural_class_name = "SalesTaxCodes"

    Query: Type[SalesTaxCodeQuery] = SalesTaxCodeQuery
    Add: Type[SalesTaxCodeAdd] = SalesTaxCodeAdd
    Mod: Type[SalesTaxCodeMod] = SalesTaxCodeMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )


@dataclass
class SalesTaxCodes(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "SalesTaxCode"
        plural_of = SalesTaxCode

    def __init__(self):
        super().__init__()


@dataclass
class CustomerSalesTaxCodeRef(QBRefMixin):
    class Meta:
        name = "CustomerSalesTaxCodeRef"


@dataclass
class ShipMethodQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "ShipMethodQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class ShipMethodAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive"
    ]

    class Meta:
        name = "ShipMethodAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 15,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class ShipMethod(QBMixinWithSave):
    class Meta:
        name = "ShipMethod"
        plural_class_name = "ShipMethods"

    Query: Type[ShipMethodQuery] = ShipMethodQuery
    Add: Type[ShipMethodAdd] = ShipMethodAdd
    # Does not have Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )


@dataclass
class ShipMethods(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "ShipMethod"
        plural_of = ShipMethod

    def __init__(self):
        super().__init__()


@dataclass
class StandardTermsQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "StandardTermsQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class StandardTermsAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "StdDueDays", "StdDiscountDays", "DiscountPct"
    ]

    class Meta:
        name = "StandardTermsAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    std_due_days: Optional[int] = field(
        default=None,
        metadata={
            "name": "StdDueDays",
            "type": "Element",
        },
    )
    std_discount_days: Optional[int] = field(
        default=None,
        metadata={
            "name": "StdDiscountDays",
            "type": "Element",
        },
    )
    discount_pct: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountPct",
            "type": "Element",
        },
    )


@dataclass
class StandardTerm(QBMixinWithSave):
    class Meta:
        name = "StandardTerms"
        plural_class_name = "StandardTerms"

    Query: Type[StandardTermsQuery] = StandardTermsQuery
    Add: Type[StandardTermsAdd] = StandardTermsAdd
    # Doesn't Have Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    std_due_days: Optional[int] = field(
        default=None,
        metadata={
            "name": "StdDueDays",
            "type": "Element",
        },
    )
    std_discount_days: Optional[int] = field(
        default=None,
        metadata={
            "name": "StdDiscountDays",
            "type": "Element",
        },
    )
    discount_pct: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountPct",
            "type": "Element",
        },
    )


@dataclass
class StandardTerms(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "StandardTerms"
        plural_of = StandardTerm

    def __init__(self):
        super().__init__()


@dataclass
class DefaultUnit(QBMixin):

    class Meta:
        name = "DefaultUnit"

    unit_used_for: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitUsedFor",
            "type": "Element",
            "required": True,
            "valid_values": ["Purchase", "Sales", "Shipping"]
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )


@dataclass
class BaseUnit(QBMixin):

    class Meta:
        name = "BaseUnit"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )


@dataclass
class RelatedUnit(QBMixin):

    class Meta:
        name = "RelatedUnit"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    conversion_ratio: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "ConversionRatio",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UnitOfMeasureSetQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "UnitOfMeasureSetQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class UnitOfMeasureSetAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "UnitOfMeasureType", "BaseUnit",
        "RelatedUnit", "DefaultUnit"
    ]

    class Meta:
        name = "UnitOfMeasureSetAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    unit_of_measure_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureType",
            "type": "Element",
            "required": True,
            "valid_values": ["Area", "Count", "Length", "Other", "Time", "Volume", "Weight"],
        },
    )
    base_unit: Optional[BaseUnit] = field(
        default=None,
        metadata={
            "name": "BaseUnit",
            "type": "Element",
            "required": True,
        },
    )
    related_unit: List[RelatedUnit] = field(
        default_factory=list,
        metadata={
            "name": "RelatedUnit",
            "type": "Element",
        },
    )
    default_unit: List[DefaultUnit] = field(
        default_factory=list,
        metadata={
            "name": "DefaultUnit",
            "type": "Element",
        },
    )


@dataclass
class UnitOfMeasureSet(QBMixinWithSave):

    class Meta:
        name = "UnitOfMeasureSet"
        plural_class_name = "UnitOfMeasureSets"

    Query: Type[UnitOfMeasureSetQuery] = UnitOfMeasureSetQuery
    Add: Type[UnitOfMeasureSetAdd] = UnitOfMeasureSetAdd
    # No Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    unit_of_measure_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureType",
            "type": "Element",
            "valid_values": ["Area", "Count", "Length", "Other", "Time", "Volume", "Weight"]
        },
    )
    base_unit: Optional[BaseUnit] = field(
        default=None,
        metadata={
            "name": "BaseUnit",
            "type": "Element",
        },
    )
    related_unit: List[RelatedUnit] = field(
        default_factory=list,
        metadata={
            "name": "RelatedUnit",
            "type": "Element",
        },
    )
    default_unit: List[DefaultUnit] = field(
        default_factory=list,
        metadata={
            "name": "DefaultUnit",
            "type": "Element",
        },
    )


@dataclass
class UnitOfMeasureSets(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "UnitOfMeasureSet"
        plural_of = UnitOfMeasureSet

    def __init__(self):
        super().__init__()


@dataclass
class VendorTypeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "VendorTypeQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default="All",
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )
    # meta_data: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #         "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
    #     },
    # )


@dataclass
class VendorTypeAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "VendorTypeAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )


@dataclass
class VendorType(QBMixinWithSave):
    class Meta:
        name = "VendorType"
        plural_class_name = "VendorTypes"

    Query: Type[VendorTypeQuery] = VendorTypeQuery
    Add: Type[VendorTypeAdd] = VendorTypeAdd
    # No Mod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    full_name: Optional[str] = field(default=None, metadata={**full_name.metadata, "max_length": 159})
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )


@dataclass
class VendorTypes(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "VendorType"
        plural_of = VendorType

    def __init__(self):
        super().__init__()


@dataclass
class VendorQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "TotalBalanceFilter", "CurrencyFilter",
        "ClassFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "VendorQuery"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    total_balance_filter: Optional[TotalBalanceFilter] = field(
        default=None,
        metadata={
            "name": "TotalBalanceFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class VendorAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ClassRef", "CompanyName", "Salutation",
        "FirstName", "MiddleName", "LastName", "JobTitle", "VendorAddress",
        "ShipAddress", "Phone", "AltPhone", "Fax", "Email",
        "Cc", "Contact", "AltContact", "AdditionalContactRef",
        "Contacts", "NameOnCheck", "AccountNumber", "Notes",
        "AdditionalNotes", "VendorTypeRef", "TermsRef", "CreditLimit",
        "VendorTaxIdent", "IsVendorEligibleFor1099", "OpenBalance",
        "OpenBalanceDate", "BillingRateRef", "ExternalGUID",
        "PrefillAccountRef", "CurrencyRef"
    ]

    class Meta:
        name = "VendorAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    additional_notes: List[AdditionalNotes] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotes",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    open_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenBalance",
            "type": "Element",
        },
    )
    open_balance_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OpenBalanceDate",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class VendorMod(QBModRqMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ClassRef",
        "CompanyName", "Salutation", "FirstName", "MiddleName",
        "LastName", "JobTitle", "VendorAddress", "ShipAddress",
        "Phone", "AltPhone", "Fax", "Email", "Cc", "Contact",
        "AltContact", "AdditionalContactRef", "ContactsMod",
        "NameOnCheck", "AccountNumber", "Notes", "AdditionalNotesMod",
        "VendorTypeRef", "TermsRef", "CreditLimit", "VendorTaxIdent",
        "IsVendorEligibleFor1099", "BillingRateRef", "PrefillAccountRef",
        "CurrencyRef"
    ]

    class Meta:
        name = "VendorMod"


    list_id: Optional[str] = field(default=None, metadata={**list_id.metadata, "required": True})
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts_mod: List[ContactsMod] = field(
        default_factory=list,
        metadata={
            "name": "ContactsMod",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    additional_notes_mod: List[AdditionalNotesMod] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesMod",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class Vendor(QBMixinWithSave):

    class Meta:
        name = "Vendor"
        plural_class_name = "Vendors"

    Query: Type[VendorQuery] = VendorQuery
    Add: Type[VendorAdd] = VendorAdd
    Mod: Type[VendorMod] = VendorMod

    list_id: Optional[str] = list_id
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    is_tax_agency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxAgency",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    vendor_address_block: Optional[VendorAddressBlock] = field(
        default=None,
        metadata={
            "name": "VendorAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    additional_notes_ret: List[AdditionalNotesRet] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesRet",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Balance",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class Vendors(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Vendor"
        plural_of = Vendor

    def __init__(self):
        super().__init__()


# endregion


# region Transactions


@dataclass
class ARRefundCreditCardQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ARRefundCreditCardQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class ARRefundCreditCardAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "RefundFromAccountRef", "ARAccountRef", "TxnDate",
        "RefNumber", "Address", "PaymentMethodRef", "Memo",
        "CreditCardTxnInfo", "ExchangeRate", "ExternalGUID",
        "RefundAppliedToTxnAdd"
    ]

    class Meta:
        name = "ARRefundCreditCardAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    refund_from_account_ref: Optional[RefundFromAccountRef] = field(
        default=None,
        metadata={
            "name": "RefundFromAccountRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    refund_applied_to_txn_add: List[RefundAppliedToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "RefundAppliedToTxnAdd",
            "type": "Element",
            "min_occurs": 1,
        },
    )

@dataclass
class ARRefundCreditCard(QBMixinWithSave):
    class Meta:
        name = "ARRefundCreditCard"
        plural_class_name = "ARRefundCreditCards"

    Query: Type[ARRefundCreditCardQuery] = ARRefundCreditCardQuery
    Add: Type[ARRefundCreditCardAdd] = ARRefundCreditCardAdd
    #No Mod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    refund_from_account_ref: Optional[RefundFromAccountRef] = field(
        default=None,
        metadata={
            "name": "RefundFromAccountRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    address_block: Optional[AddressBlock] = field(
        default=None,
        metadata={
            "name": "AddressBlock",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    refund_applied_to_txn_ret: List[RefundAppliedToTxn] = field(
        default_factory=list,
        metadata={
            "name": "RefundAppliedToTxnRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ARRefundCreditCards(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "ARRefundCreditCard"
        plural_of = ARRefundCreditCard

    def __init__(self):
        super().__init__()


@dataclass
class BillPaymentCheckQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BillPaymentCheckQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentCheckAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "PayeeEntityRef", "APAccountRef", "TxnDate", "BankAccountRef",
        "IsToBePrinted", "RefNumber", "Memo", "ExchangeRate",
        "ExternalGUID", "AppliedToTxnAdd"
    ]

    class Meta:
        name = "BillPaymentCheckAdd"

    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
            "required": True,
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
            "type": "Element",
            "required": True,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_add: List[AppliedToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnAdd",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class BillPaymentCheckMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "BankAccountRef",
        "Amount", "ExchangeRate", "IsToBePrinted", "RefNumber",
        "Memo", "AppliedToTxnMod"
    ]

    class Meta:
        name = "BillPaymentCheckMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    applied_to_txn_mod: List[AppliedToTxnMod] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnMod",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentCheck(QBMixinWithSave):
    class Meta:
        name = "BillPaymentCheck"
        plural_class_name = "BillPaymentChecks"

    Query: Type[BillPaymentCheckQuery] = BillPaymentCheckQuery
    Add: Type[BillPaymentCheckAdd] = BillPaymentCheckAdd
    Mod: Type[BillPaymentCheckMod] = BillPaymentCheckMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    address_block: Optional[AddressBlock] = field(
        default=None,
        metadata={
            "name": "AddressBlock",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_ret: List[AppliedToTxn] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentChecks(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "BillPaymentCheck"
        plural_of = BillPaymentCheck

    def __init__(self):
        super().__init__()


@dataclass
class BillPaymentCreditCardQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BillPaymentCreditCardQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentCreditCardAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "PayeeEntityRef", "APAccountRef", "TxnDate", "CreditCardAccountRef",
        "RefNumber", "Memo", "ExchangeRate", "ExternalGUID", "AppliedToTxnAdd"
    ]

    class Meta:
        name = "BillPaymentCreditCardAdd"

    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
            "required": True,
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    credit_card_account_ref: Optional[CreditCardAccountRef] = field(
        default=None,
        metadata={
            "name": "CreditCardAccountRef",
            "type": "Element",
            "required": True,
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_add: List[AppliedToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnAdd",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class BillPaymentCreditCard(QBMixinWithSave):
    class Meta:
        name = "BillPaymentCreditCard"
        plural_class_name = "BillPaymentCreditCards"

    Query: Type[BillPaymentCreditCardQuery] = BillPaymentCreditCardQuery
    Add: Type[BillPaymentCreditCardAdd] = BillPaymentCreditCardAdd
    # No Mod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    credit_card_account_ref: Optional[CreditCardAccountRef] = field(
        default=None,
        metadata={
            "name": "CreditCardAccountRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_ret: List[AppliedToTxn] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentCreditCards(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "BillPaymentCreditCard"
        plural_of = BillPaymentCreditCard

    def __init__(self):
        super().__init__()


@dataclass
class BillQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "PaidStatus", "IncludeLineItems",
        "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BillQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    paid_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaidStatus",
            "type": "Element",
            "valid_values": ["All", "PaidOnly", "NotPaidOnly"],
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class BillAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "VendorRef", "VendorAddress", "APAccountRef", "TxnDate",
        "DueDate", "RefNumber", "TermsRef", "Memo", "ExchangeRate",
        "ExternalGUID", "LinkToTxnID", "ExpenseLineAdd", "ItemLineAdd",
        "ItemGroupLineAdd"
    ]

    class Meta:
        name = "BillAdd"

    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
            "required": True,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    link_to_txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LinkToTxnID",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class BillMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "VendorRef", "VendorAddress",
        "APAccountRef", "TxnDate", "DueDate", "RefNumber",
        "TermsRef", "Memo", "ExchangeRate", "ClearExpenseLines",
        "ExpenseLineMod", "ClearItemLines", "ItemLineMod",
        "ItemGroupLineMod"
    ]

    class Meta:
        name = "BillMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )


@dataclass
class Bill(QBMixinWithSave):

    class Meta:
        name = "Bill"
        plural_class_name = "Bills"

    Query: Type[BillQuery] = BillQuery
    Add: Type[BillAdd] = BillAdd
    Mod: Type[BillMod] = BillMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    amount_due: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountDue",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_due_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountDueInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_paid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPaid",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    expense_line: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_lines: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_lines: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
            "type": "Element",
        },
    )
    open_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenAmount",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class Bills(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Bill"
        plural_of = Bill

    def __init__(self):
        super().__init__()


@dataclass
class BuildAssemblyQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "ItemFilter",
        "RefNumberFilter", "RefNumberRangeFilter", "PendingStatus",
        "IncludeComponentLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BuildAssemblyQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    item_filter: Optional[ItemFilter] = field(
        default=None,
        metadata={
            "name": "ItemFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    pending_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PendingStatus",
            "type": "Element",
            "valid_values": ["All", "PendingOnly", "NotPendingOnly"],
        },
    )
    include_component_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeComponentLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class BuildAssemblyAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "ItemInventoryAssemblyRef", "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "TxnDate", "RefNumber", "Memo", "QuantityToBuild", "MarkPendingIfRequired",
        "ExternalGUID"
    ]

    class Meta:
        name = "BuildAssemblyAdd"

    item_inventory_assembly_ref: Optional[ItemInventoryAssemblyRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryAssemblyRef",
            "type": "Element",
            "required": True,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
            "required": True,
        },
    )
    mark_pending_if_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MarkPendingIfRequired",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class BuildAssemblyMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "TxnDate", "RefNumber", "Memo", "QuantityToBuild", "MarkPendingIfRequired",
        "RemovePending"
    ]

    class Meta:
        name = "BuildAssemblyMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
        },
    )
    mark_pending_if_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MarkPendingIfRequired",
            "type": "Element",
        },
    )
    remove_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RemovePending",
            "type": "Element",
        },
    )


@dataclass
class BuildAssembly(QBMixinWithSave):
    class Meta:
        name = "BuildAssembly"
        plural_class_name = "BuildAssemblies"

    Query: Type[BuildAssemblyQuery] = BuildAssemblyQuery
    Add: Type[BuildAssemblyAdd] = BuildAssemblyAdd
    Mod: Type[BuildAssemblyMod] = BuildAssemblyMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    item_inventory_assembly_ref: Optional[ItemInventoryAssemblyRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryAssemblyRef",
            "type": "Element",
            "required": True,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
            "required": True,
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
            "required": True,
        },
    )
    quantity_can_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityCanBuild",
            "type": "Element",
            "required": True,
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
            "required": True,
        },
    )
    quantity_on_sales_order: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
            "type": "Element",
            "required": True,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    component_item_lines: List[ComponentItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ComponentItemLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class BuildAssemblies(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "BuildAssembly"
        plural_of = BuildAssembly

    def __init__(self):
        super().__init__()


@dataclass
class ChargeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "DateMacro", "EntityFilter", "AccountFilter", "RefNumberFilter",
        "RefNumberRangeFilter", "PaidStatus", "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ChargeQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    paid_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaidStatus",
            "type": "Element",
            "valid_values": ["All", "PaidOnly", "NotPaidOnly"],
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class ChargeAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "TxnDate", "RefNumber", "ItemRef", "InventorySiteRef",
        "InventorySiteLocationRef", "Quantity", "UnitOfMeasure", "Rate",
        "OptionForPriceRuleConflict", "Amount", "Desc", "ARAccountRef",
        "ClassRef", "BilledDate", "DueDate", "OverrideItemAccountRef",
        "ExternalGUID"
    ]

    class Meta:
        name = "ChargeAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"],
            },
        )
    )
    amount: Optional[Decimal] = amount
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    billed_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "BilledDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class ChargeMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "TxnDate", "RefNumber",
        "ItemRef", "InventorySiteRef", "InventorySiteLocationRef", "Quantity",
        "UnitOfMeasure", "OverrideUOMSetRef", "Rate", "OptionForPriceRuleConflict",
        "Amount", "Desc", "ARAccountRef", "ClassRef", "BilledDate", "DueDate",
        "OverrideItemAccountRef"
    ]

    class Meta:
        name = "ChargeMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    amount: Optional[Decimal] = amount
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    billed_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "BilledDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )


@dataclass
class Charge(QBMixinWithSave):
    class Meta:
        name = "Charge"
        plural_class_name = "Charges"

    Query: Type[ChargeQuery] = ChargeQuery
    Add: Type[ChargeAdd] = ChargeAdd
    Mod: Type[ChargeMod] = ChargeMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    balance_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    billed_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "BilledDate",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    is_paid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPaid",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Charges(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "Charge"
        plural_of = Charge

    def __init__(self):
        super().__init__()


@dataclass
class ApplyCheckToTxnBase:
    class Meta:
        name = ""

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class ApplyCheckToTxnAdd(ApplyCheckToTxnBase, QBAddRqMixin):
    class Meta:
        name = "ApplyCheckToTxnAdd"


@dataclass
class ApplyCheckToTxnMod(ApplyCheckToTxnBase, QBAddRqMixin):
    class Meta:
        name = "ApplyCheckToTxnMod"


@dataclass
class CheckQuery(QBQueryMixin):
    FIELD_ORDER = [
        "metaData", "iterator", "iteratorID", "TxnID", "RefNumber",
        "RefNumberCaseSensitive", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "EntityFilter", "AccountFilter", "RefNumberFilter",
        "RefNumberRangeFilter", "CurrencyFilter", "IncludeLineItems",
        "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "CheckQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class CheckAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "defMacro", "AccountRef", "PayeeEntityRef", "RefNumber", "TxnDate",
        "Memo", "Address", "IsToBePrinted", "ExchangeRate", "ExternalGUID",
        "ApplyCheckToTxnAdd", "ExpenseLineAdd", "ItemLineAdd", "ItemGroupLineAdd"
    ]

    class Meta:
        name = "CheckAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    apply_check_to_txn_add: List[ApplyCheckToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "ApplyCheckToTxnAdd",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class CheckMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "PayeeEntityRef", "RefNumber",
        "TxnDate", "Memo", "Address", "IsToBePrinted", "ExchangeRate",
        "ApplyCheckToTxnMod", "ClearExpenseLines", "ExpenseLineMod",
        "ClearItemLines", "ItemLineMod", "ItemGroupLineMod"
    ]

    class Meta:
        name = "CheckMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    apply_check_to_txn_mod: List[ApplyCheckToTxnMod] = field(
        default_factory=list,
        metadata={
            "name": "ApplyCheckToTxnMod",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )


@dataclass
class Check(QBMixinWithSave):
    class Meta:
        name = "Check"
        plural_class_name = "Checks"

    Query: Type[CheckQuery] = CheckQuery
    Add: Type[CheckAdd] = CheckAdd
    Mod: Type[CheckMod] = CheckMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    address_block: Optional[AddressBlock] = field(
        default=None,
        metadata={
            "name": "AddressBlock",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    expense_lines: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_lines: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_lines: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Checks(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "Check"
        plural_of = Check

    def __init__(self):
        super().__init__()


@dataclass
class CreditCardChargeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "CreditCardChargeQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class CreditCardChargeAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "AccountRef", "PayeeEntityRef", "TxnDate", "RefNumber", "Memo",
        "ExchangeRate", "ExternalGUID", "ExpenseLineAdd", "ItemLineAdd",
        "ItemGroupLineAdd"
    ]

    class Meta:
        name = "CreditCardChargeAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class CreditCardChargeMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "PayeeEntityRef", "TxnDate",
        "RefNumber", "Memo", "ExchangeRate", "ClearExpenseLines",
        "ExpenseLineMod", "ClearItemLines", "ItemLineMod", "ItemGroupLineMod"
    ]

    class Meta:
        name = "CreditCardChargeMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )


@dataclass
class CreditCardCharge(QBMixinWithSave):
    class Meta:
        name = "CurrencyFilter"
        plural_class_name = "CurrencyFilters"

    Query: Type[CreditCardChargeQuery] = CreditCardChargeQuery
    Add: Type[CreditCardChargeAdd] = CreditCardChargeAdd
    Mod: Type[CreditCardChargeMod] = CreditCardChargeMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    expense_lines: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_lines: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_lines: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class CreditCardCharges(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "CreditCardCharge"
        plural_of = CreditCardCharge

    def __init__(self):
        super().__init__()


@dataclass
class CreditCardCreditQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "CreditCardCreditQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class CreditCardCreditAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "AccountRef", "PayeeEntityRef", "TxnDate", "RefNumber", "Memo",
        "ExchangeRate", "ExternalGUID", "ExpenseLineAdd", "ItemLineAdd",
        "ItemGroupLineAdd"
    ]

    class Meta:
        name = "CreditCardCreditAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class CreditCardCreditMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "PayeeEntityRef", "TxnDate",
        "RefNumber", "Memo", "ExchangeRate", "ClearExpenseLines",
        "ExpenseLineMod", "ClearItemLines", "ItemLineMod", "ItemGroupLineMod"
    ]

    class Meta:
        name = "CreditCardCreditMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )


@dataclass
class CreditCardCredit(QBMixinWithSave):
    class Meta:
        name = "CreditCardCredits"
        plural_class_name = "CreditCardCredits"

    Query: Type[CreditCardCreditQuery] = CreditCardCreditQuery
    Add: Type[CreditCardCreditAdd] = CreditCardCreditAdd
    Mod: Type[CreditCardCreditMod] = CreditCardCreditMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    expense_lines: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_lines: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_lines: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class CreditCardCredits(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "CreditCardCredit"
        plural_of = CreditCardCredit

    def __init__(self):
        super().__init__()


@dataclass
class CreditMemoQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeLinkedTxns",
        "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "CreditMemoQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "ClassRef", "ARAccountRef", "TemplateRef", "TxnDate", "RefNumber",
        "BillAddress", "ShipAddress", "IsPending", "PONumber", "TermsRef", "DueDate",
        "SalesRepRef", "FOB", "ShipDate", "ShipMethodRef", "ItemSalesTaxRef", "Memo",
        "CustomerMsgRef", "IsToBePrinted", "IsToBeEmailed", "CustomerSalesTaxCodeRef",
        "Other", "ExchangeRate", "ExternalGUID", "CreditMemoLineAdd", "CreditMemoLineGroupAdd"
    ]

    class Meta:
        name = "CreditMemoAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    credit_memo_line_add: List[CreditMemoLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineAdd",
            "type": "Element",
        },
    )
    credit_memo_line_group_add: List[CreditMemoLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineGroupAdd",
            "type": "Element",
        },
    )


@dataclass
class CreditMemoMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "ARAccountRef", "TemplateRef",
        "TxnDate", "RefNumber", "BillAddress", "ShipAddress", "IsPending", "PONumber",
        "TermsRef", "DueDate", "SalesRepRef", "FOB", "ShipDate", "ShipMethodRef",
        "ItemSalesTaxRef", "Memo", "CustomerMsgRef", "IsToBePrinted", "IsToBeEmailed",
        "CustomerSalesTaxCodeRef", "Other", "ExchangeRate", "CreditMemoLineMod",
        "CreditMemoLineGroupMod"
    ]

    class Meta:
        name = "CreditMemoMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    credit_memo_line_mod: List[CreditMemoLineMod] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineMod",
            "type": "Element",
        },
    )
    credit_memo_line_group_mod: List[CreditMemoLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class CreditMemo(QBMixinWithSave):
    class Meta:
        name = "CreditMemo"
        plural_class_name = "CreditMemos"

    Query: Type[CreditMemoQuery] = CreditMemoQuery
    Add: Type[CreditMemoAdd] = CreditMemoAdd
    Mod: Type[CreditMemoMod] = CreditMemoMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    credit_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemaining",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    credit_remaining_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemainingInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    credit_memo_lines: List[CreditMemoLine] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineRet",
            "type": "Element",
        },
    )
    credit_memo_line_group_ret: List[CreditMemoLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "CreditMemoLineGroupRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class CreditMemos(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "CreditMemo"
        plural_of = CreditMemo

    def __init__(self):
        super().__init__()


@dataclass
class CashBackInfoAdd(QBMixin):
    FIELD_ORDER = [
        "AccountRef", "Memo", "Amount"
    ]

    class Meta:
        name = "CashBackInfoAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class CashBackInfoMod(QBModRqMixin):
    FIELD_ORDER = [
        "AccountRef", "Memo", "Amount"
    ]

    class Meta:
        name = "CashBackInfoMod"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class CashBackInfo(QBMixin):
    FIELD_ORDER = [
        "txn_line_id", "AccountRef", "Memo", "Amount"
    ]

    class Meta:
        name = "CashBackInfo"
        plural_class_name = "CashBackInfo"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    amount: Optional[Decimal] = amount


@dataclass
class DepositQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "DepositQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class DepositAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "TxnDate", "DepositToAccountRef", "Memo", "CashBackInfoAdd", "CurrencyRef",
        "ExchangeRate", "ExternalGUID", "DepositLineAdd"
    ]

    class Meta:
        name = "DepositAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
            "required": True,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    cash_back_info_add: Optional[CashBackInfoAdd] = field(
        default=None,
        metadata={
            "name": "CashBackInfoAdd",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    deposit_line_add: List[DepositLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class DepositMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "DepositToAccountRef", "Memo",
        "CashBackInfoMod", "CurrencyRef", "ExchangeRate", "DepositLineMod"
    ]

    class Meta:
        name = "DepositMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    cash_back_info_mod: Optional[CashBackInfoMod] = field(
        default=None,
        metadata={
            "name": "CashBackInfoMod",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    deposit_line_mod: List[DepositLineMod] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineMod",
            "type": "Element",
        },
    )


@dataclass
class Deposit(QBMixinWithSave):
    class Meta:
        name = "Deposit"
        plural_class_name = "Deposits"

    Query: Type[DepositQuery] = DepositQuery
    Add: Type[DepositAdd] = DepositAdd
    Mod: Type[DepositMod] = DepositMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DepositTotal",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    deposit_total_in_home_currency: Optional[Decimal] = (
        field(
            default=None,
            metadata={
                "name": "DepositTotalInHomeCurrency",
                "type": "Element",
            },
        )
    )
    cash_back_info_ret: Optional[CashBackInfo] = field(
        default=None,
        metadata={
            "name": "CashBackInfoRet",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    deposit_lines: List[DepositLine] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Deposits(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "Deposit"
        plural_of = Deposit

    def __init__(self):
        super().__init__()


@dataclass
class EstimateQuery(QBQueryMixin):
    FIELD_ORDER = [
        "metaData", "iterator", "iteratorID", "TxnID", "RefNumber", "RefNumberCaseSensitive",
        "MaxReturned", "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter", "CurrencyFilter",
        "IncludeLineItems", "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "EstimateQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    # request_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "requestID",
    #         "type": "Attribute",
    #     },
    # )


@dataclass
class EstimateAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "ClassRef", "TemplateRef", "TxnDate", "RefNumber",
        "BillAddress", "ShipAddress", "IsActive", "PONumber", "TermsRef", "DueDate",
        "SalesRepRef", "FOB", "ItemSalesTaxRef", "Memo", "CustomerMsgRef",
        "IsToBeEmailed", "CustomerSalesTaxCodeRef", "Other", "ExchangeRate",
        "ExternalGUID", "EstimateLineAdd", "EstimateLineGroupAdd"
    ]

    class Meta:
        name = "EstimateAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    estimate_line_add: List[EstimateLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineAdd",
            "type": "Element",
        },
    )
    estimate_line_group_add: List[EstimateLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineGroupAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class EstimateMod(QBMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "TemplateRef", "TxnDate",
        "RefNumber", "BillAddress", "ShipAddress", "IsActive", "CreateChangeOrder",
        "PONumber", "TermsRef", "DueDate", "SalesRepRef", "FOB", "ItemSalesTaxRef",
        "Memo", "CustomerMsgRef", "IsToBeEmailed", "CustomerSalesTaxCodeRef",
        "Other", "ExchangeRate", "EstimateLineMod", "EstimateLineGroupMod"
    ]

    class Meta:
        name = "EstimateMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    create_change_order: Optional[bool] = field(
        default=None,
        metadata={
            "name": "CreateChangeOrder",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    estimate_line_mod: List[EstimateLineMod] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineMod",
            "type": "Element",
        },
    )
    estimate_line_group_mod: List[EstimateLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class Estimate(QBMixinWithSave):
    class Meta:
        name = "Estimate"
        plural_class_name = "Estimates"

    Query: Type[EstimateQuery] = EstimateQuery
    Add: Type[EstimateAdd] = EstimateAdd
    Mod: Type[EstimateMod] = EstimateMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    estimate_lines: List[EstimateLine] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineRet",
            "type": "Element",
        },
    )
    estimate_line_group_ret: List[EstimateLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "EstimateLineGroupRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Estimates(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "Estimate"
        plural_of = Estimate

    def __init__(self):
        super().__init__()


@dataclass
class InventoryAdjustmentQuery(QBQueryMixin):
    FIELD_ORDER = [
        "metaData", "iterator", "iteratorID", "TxnID", "RefNumber", "RefNumberCaseSensitive",
        "MaxReturned", "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "ItemFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "InventoryAdjustmentQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    item_filter: Optional[ItemFilter] = field(
        default=None,
        metadata={
            "name": "ItemFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "defMacro", "AccountRef", "TxnDate", "RefNumber", "InventorySiteRef",
        "CustomerRef", "ClassRef", "Memo", "ExternalGUID", "InventoryAdjustmentLineAdd"
    ]

    class Meta:
        name = "InventoryAdjustmentAdd"

    account_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    inventory_adjustment_line_add: List[InventoryAdjustmentLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineAdd",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class InventoryAdjustmentMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "InventorySiteRef", "TxnDate",
        "RefNumber", "CustomerRef", "ClassRef", "Memo", "InventoryAdjustmentLineMod"
    ]

    class Meta:
        name = "InventoryAdjustmentMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    inventory_adjustment_line_mod: List[InventoryAdjustmentLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineMod",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustment(QBMixinWithSave):
    class Meta:
        name = "InventoryAdjustment"
        plural_class_name = "InventoryAdjustments"

    Query: Type[InventoryAdjustmentQuery] = InventoryAdjustmentQuery
    Add: Type[InventoryAdjustmentAdd] = InventoryAdjustmentAdd
    Mod: Type[InventoryAdjustmentMod] = InventoryAdjustmentMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    inventory_adjustment_lines: List[InventoryAdjustmentLine] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustments(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "InventoryAdjustment"
        plural_of = InventoryAdjustment

    def __init__(self):
        super().__init__()


@dataclass
class InvoiceQuery(QBQueryMixin):

    FIELD_ORDER = [
        "txn_id", "ref_number", "ref_number_case_sensitive", "max_returned",
        "modified_date_range_filter", "txn_date_range_filter", "entity_filter",
        "account_filter", "ref_number_filter", "ref_number_range_filter",
        "currency_filter", "paid_status", "include_line_items", "include_linked_txns",
        "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "InvoiceQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    paid_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaidStatus",
            "type": "Element",
            "valid_values": ["All", "PaidOnly", "NotPaidOnly"]
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class InvoiceAdd(QBAddRqMixin):

    FIELD_ORDER = [
        "customer_ref", "class_ref", "ar_account_ref", "template_ref", "txn_date",
        "ref_number", "bill_address", "ship_address", "is_pending", "is_finance_charge",
        "po_number", "terms_ref", "due_date", "sales_rep_ref", "fob", "ship_date",
        "ship_method_ref", "item_sales_tax_ref", "memo", "customer_msg_ref",
        "is_to_be_printed", "is_to_be_emailed", "customer_sales_tax_code_ref",
        "other", "exchange_rate", "external_guid", "link_to_txn_id", "set_credit",
        "invoice_line_add", "invoice_line_group_add", "include_ret_element"
    ]

    class Meta:
        name = "InvoiceAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    is_finance_charge: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFinanceCharge",
            "type": "Element",
        },
    )
    po_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    link_to_txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LinkToTxnID",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    invoice_line_add: List[InvoiceLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineAdd",
            "type": "Element",
        },
    )
    invoice_line_group_add: List[InvoiceLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupAdd",
            "type": "Element",
        },
    )

    def validate(self):
        super().validate()
        self.is_to_be_emailed = False
        self.is_pending = False
        self.is_to_be_printed = False


@dataclass
class InvoiceMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "ARAccountRef",
        "TemplateRef", "TxnDate", "RefNumber", "BillAddress", "ShipAddress",
        "IsPending", "PONumber", "TermsRef", "DueDate", "SalesRepRef",
        "FOB", "ShipDate", "ShipMethodRef", "ItemSalesTaxRef", "Memo",
        "CustomerMsgRef", "IsToBePrinted", "IsToBeEmailed",
        "CustomerSalesTaxCodeRef", "Other", "ExchangeRate", "SetCredit",
        "InvoiceLineMod", "InvoiceLineGroupMod"
    ]

    class Meta:
        name = "InvoiceMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    invoice_line_mod: List[InvoiceLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineMod",
            "type": "Element",
        },
    )
    invoice_line_group_mod: List[InvoiceLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class Invoice(QBMixinWithSave):

    class Meta:
        name = "Invoice"
        plural_class_name = "Invoices"

    Query: Type[InvoiceQuery] = InvoiceQuery
    Add: Type[InvoiceAdd] = InvoiceAdd
    Mod: Type[InvoiceMod] = InvoiceMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    ar_account_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    is_finance_charge: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFinanceCharge",
            "type": "Element",
        },
    )
    po_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    applied_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
        },
    )
    balance_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    balance_remaining_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemainingInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    is_paid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPaid",
            "type": "Element",
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    suggested_discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountAmount",
            "type": "Element",
        },
    )
    suggested_discount_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountDate",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    invoice_lines: List[InvoiceLine] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineRet",
            "type": "Element",
        },
    )
    invoice_line_group_ret: List[InvoiceLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupRet",
            "type": "Element",
        },
    )

    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class Invoices(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Invoice"
        plural_of = Invoice

    def __init__(self):
        super().__init__()

    def split_invoices_by_tax(self) -> Dict[str, List[Invoice]]:
        result = defaultdict(list)

        # Group invoices by item_sales_tax_ref and sales_tax_percentage
        for invoice in self:  # Assuming self.invoices holds the list of Invoice objects
            key = f"{invoice.item_sales_tax_ref}-{invoice.sales_tax_percentage}"
            result[key].append(invoice)

        return dict(result)



@dataclass
class JournalEntryQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "EntityFilter", "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "JournalEntryQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class JournalEntryAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "TxnDate", "RefNumber", "IsAdjustment", "IsHomeCurrencyAdjustment",
        "IsAmountsEnteredInHomeCurrency", "CurrencyRef", "ExchangeRate",
        "ExternalGUID", "JournalDebitLine", "JournalCreditLine"
    ]

    class Meta:
        name = "JournalEntryAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
        },
    )
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    #todo: is_home_currency_adjustment and is_amounts_entered_in_home_currency/currency_ref are part of an "or".
    #       So they can't both be in the add xml at the same time.
    # is_home_currency_adjustment: Optional[bool] = field(
    #     default=None,
    #     metadata={
    #         "name": "IsHomeCurrencyAdjustment",
    #         "type": "Element",
    #     },
    # )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    journal_debit_lines: List[JournalDebitLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalDebitLine",
            "type": "Element",
        },
    )
    journal_credit_lines: List[JournalCreditLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalCreditLine",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class JournalEntryMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "RefNumber", "IsAdjustment",
        "IsAmountsEnteredInHomeCurrency", "CurrencyRef", "ExchangeRate",
        "JournalLineMod"
    ]

    class Meta:
        name = "JournalEntryMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    journal_line_mod: List[JournalLineMod] = field(
        default_factory=list,
        metadata={
            "name": "JournalLineMod",
            "type": "Element",
        },
    )


@dataclass
class JournalEntry(QBMixinWithSave):
    class Meta:
        name = "JournalEntry"
        plural_class_name = "JournalEntries"

    Query: Type[JournalEntryQuery] = JournalEntryQuery
    Add: Type[JournalEntryAdd] = JournalEntryAdd
    Mod: Type[JournalEntryMod] = JournalEntryMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
        },
    )
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    is_home_currency_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsHomeCurrencyAdjustment",
            "type": "Element",
        },
    )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    journal_debit_lines: List[JournalDebitLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalDebitLine",
            "type": "Element",
        },
    )
    journal_credit_lines: List[JournalCreditLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalCreditLine",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class JournalEntries(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "JournalEntry"
        plural_of = JournalEntry

    def __init__(self):
        super().__init__()


@dataclass
class ShipToEntityRef(QBRefMixin):
    class Meta:
        name = "ShipToEntityRef"


@dataclass
class PurchaseOrderQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeLinkedTxns",
        "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "PurchaseOrderQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "VendorRef", "ClassRef", "InventorySiteRef", "ShipToEntityRef",
        "TemplateRef", "TxnDate", "RefNumber", "VendorAddress",
        "ShipAddress", "TermsRef", "DueDate", "ExpectedDate",
        "ShipMethodRef", "FOB", "Memo", "VendorMsg", "IsToBePrinted",
        "IsToBeEmailed", "Other1", "Other2", "ExchangeRate",
        "ExternalGUID", "PurchaseOrderLineAdd", "PurchaseOrderLineGroupAdd"
    ]

    class Meta:
        name = "PurchaseOrderAdd"

    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    purchase_order_line_add: List[PurchaseOrderLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineAdd",
            "type": "Element",
        },
    )
    purchase_order_line_group_add: List[PurchaseOrderLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class PurchaseOrderMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "VendorRef", "ClassRef", "InventorySiteRef",
        "ShipToEntityRef", "TemplateRef", "TxnDate", "RefNumber", "VendorAddress",
        "ShipAddress", "TermsRef", "DueDate", "ExpectedDate", "ShipMethodRef",
        "FOB", "IsManuallyClosed", "Memo", "VendorMsg", "IsToBePrinted",
        "IsToBeEmailed", "Other1", "Other2", "ExchangeRate",
        "PurchaseOrderLineMod", "PurchaseOrderLineGroupMod"
    ]

    class Meta:
        name = "PurchaseOrderMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    purchase_order_line_mod: List[PurchaseOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineMod",
            "type": "Element",
        },
    )
    purchase_order_line_group_mod: List[PurchaseOrderLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupMod",
            "type": "Element",
        },
    )

@dataclass
class PurchaseOrder(QBMixinWithSave):

    class Meta:
        name = "PurchaseOrder"
        plural_class_name = "PurchaseOrders"

    Query: Type[PurchaseOrderQuery] = PurchaseOrderQuery
    Add: Type[PurchaseOrderAdd] = PurchaseOrderAdd
    Mod: Type[PurchaseOrderMod] = PurchaseOrderMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    vendor_address_block: Optional[VendorAddressBlock] = field(
        default=None,
        metadata={
            "name": "VendorAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    is_fully_received: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFullyReceived",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    purchase_order_lines: List[PurchaseOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineRet",
            "type": "Element",
        },
    )
    purchase_order_line_group_ret: List[PurchaseOrderLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrders(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "PurchaseOrder"
        plural_of = PurchaseOrder

    def __init__(self):
        super().__init__()


@dataclass
class CreditCardTxnInputInfoMod(QBMixin):
    FIELD_ORDER = [
        "CreditCardNumber", "ExpirationMonth", "ExpirationYear", "NameOnCard",
        "CreditCardAddress", "CreditCardPostalCode", "CommercialCardCode",
        "TransactionMode", "CreditCardTxnType"
    ]

    class Meta:
        name = "CreditCardTxnInputInfoMod"

    credit_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    expiration_month: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationMonth",
            "type": "Element",
            "valid_values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        },
    )
    expiration_year: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationYear",
            "type": "Element",
        },
    )
    name_on_card: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCard",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardAddress",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardPostalCode",
            "type": "Element",
            "max_length": 18,
        },
    )
    commercial_card_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CommercialCardCode",
            "type": "Element",
            "max_length": 24,
        },
    )
    transaction_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionMode",
            "type": "Element",
            "valid_values": ["CardNotPresent", "CardPresent"]
        },
    )
    credit_card_txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnType",
            "type": "Element",
            "valid_values": ["Authorization", "Capture", "Charge", "Refund", "VoiceAuthorization"]
        },
    )


@dataclass
class CreditCardTxnResultInfoMod(QBMixin):
    FIELD_ORDER = [
        "ResultCode", "ResultMessage", "CreditCardTransID", "MerchantAccountNumber",
        "AuthorizationCode", "AVSStreet", "AVSZip", "CardSecurityCodeMatch",
        "ReconBatchID", "PaymentGroupingCode", "PaymentStatus",
        "TxnAuthorizationTime", "TxnAuthorizationStamp", "ClientTransID"
    ]

    class Meta:
        name = "CreditCardTxnResultInfoMod"

    result_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "ResultCode",
            "type": "Element",
        },
    )
    result_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultMessage",
            "type": "Element",
            "max_length": 60,
        },
    )
    credit_card_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTransID",
            "type": "Element",
            "max_length": 24,
        },
    )
    merchant_account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "MerchantAccountNumber",
            "type": "Element",
            "max_length": 32,
        },
    )
    authorization_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuthorizationCode",
            "type": "Element",
            "max_length": 12,
        },
    )
    avsstreet: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSStreet",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    avszip: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSZip",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    card_security_code_match: Optional[str] = field(
        default=None,
        metadata={
            "name": "CardSecurityCodeMatch",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    recon_batch_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReconBatchID",
            "type": "Element",
            "max_length": 84,
        },
    )
    payment_grouping_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "PaymentGroupingCode",
            "type": "Element",
        },
    )
    payment_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentStatus",
            "type": "Element",
            "valid_values": ["Unknown", "Completed"],
        },
    )
    txn_authorization_time: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationTime",
            "type": "Element",
        },
    )
    txn_authorization_stamp: Optional[int] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationStamp",
            "type": "Element",
        },
    )
    client_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientTransID",
            "type": "Element",
            "max_length": 16,
        },
    )


@dataclass
class CreditCardTxnInfoMod(QBMixin):
    credit_card_txn_input_info_mod: Optional[CreditCardTxnInputInfoMod] = (
        field(
            default=None,
            metadata={
                "name": "CreditCardTxnInputInfoMod",
                "type": "Element",
            },
        )
    )
    credit_card_txn_result_info_mod: Optional[CreditCardTxnResultInfoMod] = (
        field(
            default=None,
            metadata={
                "name": "CreditCardTxnResultInfoMod",
                "type": "Element",
            },
        )
    )


@dataclass
class ReceivePaymentQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ReceivePaymentQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class ReceivePaymentAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "ARAccountRef", "TxnDate", "RefNumber", "TotalAmount",
        "ExchangeRate", "PaymentMethodRef", "Memo", "DepositToAccountRef",
        "CreditCardTxnInfo", "ExternalGUID", "IsAutoApply", "AppliedToTxnAdd"
    ]

    class Meta:
        name = "ReceivePaymentAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    is_auto_apply: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAutoApply",
            "type": "Element",
        },
    )
    applied_to_txn_add: List[AppliedToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class ReceivePaymentMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ARAccountRef", "TxnDate", "RefNumber",
        "TotalAmount", "ExchangeRate", "PaymentMethodRef", "Memo", "DepositToAccountRef",
        "CreditCardTxnInfoMod", "AppliedToTxnMod"
    ]

    class Meta:
        name = "ReceivePaymentMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info_mod: Optional[CreditCardTxnInfoMod] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfoMod",
            "type": "Element",
        },
    )
    applied_to_txn_mod: List[AppliedToTxnMod] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnMod",
            "type": "Element",
        },
    )


@dataclass
class ReceivePayment(QBMixinWithSave):
    class Meta:
        name = "ReceivePayment"
        plural_class_name = "ReceivePayments"

    Query: Type[ReceivePaymentQuery] = ReceivePaymentQuery
    Add: Type[ReceivePaymentAdd] = ReceivePaymentAdd
    Mod: Type[ReceivePaymentMod] = ReceivePaymentMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    unused_payment: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "UnusedPayment",
            "type": "Element",
        },
    )
    unused_credits: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "UnusedCredits",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_ret: List[AppliedToTxn] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ReceivePayments(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "ReceivePayment"
        plural_of = ReceivePayment

    def __init__(self):
        super().__init__()


@dataclass
class SalesOrderQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "RefNumberFilter", "RefNumberRangeFilter", "CurrencyFilter",
        "IncludeLineItems", "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "SalesOrderQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "ClassRef", "TemplateRef", "TxnDate", "RefNumber", "BillAddress",
        "ShipAddress", "PONumber", "TermsRef", "DueDate", "SalesRepRef", "FOB", "ShipDate",
        "ShipMethodRef", "ItemSalesTaxRef", "IsManuallyClosed", "Memo", "CustomerMsgRef",
        "IsToBePrinted", "IsToBeEmailed", "CustomerSalesTaxCodeRef", "Other", "ExchangeRate",
        "ExternalGUID", "SalesOrderLineAdd", "SalesOrderLineGroupAdd"
    ]

    class Meta:
        name = "SalesOrderAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    sales_order_line_add: List[SalesOrderLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineAdd",
            "type": "Element",
        },
    )
    sales_order_line_group_add: List[SalesOrderLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineGroupAdd",
            "type": "Element",
        },
    )


@dataclass
class SalesOrderMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "TemplateRef", "TxnDate",
        "RefNumber", "BillAddress", "ShipAddress", "PONumber", "TermsRef", "DueDate",
        "SalesRepRef", "FOB", "ShipDate", "ShipMethodRef", "ItemSalesTaxRef",
        "IsManuallyClosed", "Memo", "CustomerMsgRef", "IsToBePrinted", "IsToBeEmailed",
        "CustomerSalesTaxCodeRef", "Other", "ExchangeRate", "SalesOrderLineMod",
        "SalesOrderLineGroupMod"
    ]

    class Meta:
        name = "SalesOrderMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    sales_order_line_mod: List[SalesOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineMod",
            "type": "Element",
        },
    )
    sales_order_line_group_mod: List[SalesOrderLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class SalesOrder(QBMixinWithSave):
    class Meta:
        name = "SalesOrder"
        plural_class_name = "SalesOrders"

    Query: Type[SalesOrderQuery] = SalesOrderQuery
    Add: Type[SalesOrderAdd] = SalesOrderAdd
    Mod: Type[SalesOrderMod] = SalesOrderMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    is_fully_invoiced: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFullyInvoiced",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    sales_order_lines: List[SalesOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineRet",
            "type": "Element",
        },
    )
    sales_order_line_group_ret: List[SalesOrderLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "SalesOrderLineGroupRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesOrders(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "SalesOrder"
        plural_of = SalesOrder

    def __init__(self):
        super().__init__()


@dataclass
class SalesReceiptQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "SalesReceiptQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "CustomerRef", "ClassRef", "TemplateRef", "TxnDate", "RefNumber",
        "BillAddress", "ShipAddress", "IsPending", "CheckNumber",
        "PaymentMethodRef", "DueDate", "SalesRepRef", "ShipDate",
        "ShipMethodRef", "FOB", "ItemSalesTaxRef", "Memo", "CustomerMsgRef",
        "IsToBePrinted", "IsToBeEmailed", "CustomerSalesTaxCodeRef",
        "DepositToAccountRef", "CreditCardTxnInfo", "Other", "ExchangeRate",
        "ExternalGUID", "SalesReceiptLineAdd", "SalesReceiptLineGroupAdd"
    ]

    class Meta:
        name = "SalesReceiptAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    sales_receipt_line_add: List[SalesReceiptLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineAdd",
            "type": "Element",
        },
    )
    sales_receipt_line_group_add: List[SalesReceiptLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupAdd",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptMod(QBModRqMixin):
    FIELD_ORDER_SALES_RECEIPT_MOD = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "TemplateRef", "TxnDate",
        "RefNumber", "BillAddress", "ShipAddress", "IsPending", "CheckNumber",
        "PaymentMethodRef", "DueDate", "SalesRepRef", "ShipDate", "ShipMethodRef",
        "FOB", "ItemSalesTaxRef", "Memo", "CustomerMsgRef", "IsToBePrinted",
        "IsToBeEmailed", "CustomerSalesTaxCodeRef", "DepositToAccountRef",
        "Other", "ExchangeRate", "SalesReceiptLineMod", "SalesReceiptLineGroupMod"
    ]

    class Meta:
        name = "SalesReceiptMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    sales_receipt_line_mod: List[SalesReceiptLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineMod",
            "type": "Element",
        },
    )
    sales_receipt_line_group_mod: List[SalesReceiptLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class SalesReceipt(QBMixinWithSave):
    class Meta:
        name = "SalesReceipt"
        plural_class_name = "SalesReceipts"

    Query: Type[SalesReceiptQuery] = SalesReceiptQuery
    Add: Type[SalesReceiptAdd] = SalesReceiptAdd
    Mod: Type[SalesReceiptMod] = SalesReceiptMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    sales_receipt_lines: List[SalesReceiptLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineRet",
            "type": "Element",
        },
    )
    sales_receipt_line_group_ret: List[SalesReceiptLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class SalesReceipts(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "SalesReceipt"
        plural_of = SalesReceipt

    def __init__(self):
        super().__init__()


@dataclass
class TimeTrackingEntityFilter(QBMixin):
    FIELD_ORDER = [
        "ListId", "FullName",
    ]

    class Meta:
        name = "TimeTrackingEntityFilter"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names


@dataclass
class TimeTrackingQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "TimeTrackingEntityFilter",
        "IncludeRetElement"
    ]

    class Meta:
        name = "TimeTrackingQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    time_tracking_entity_filter: Optional[TimeTrackingEntityFilter] = field(
        default=None,
        metadata={
            "name": "TimeTrackingEntityFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class TimeTrackingAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "TxnDate", "EntityRef", "CustomerRef", "ItemServiceRef",
        "Duration", "ClassRef", "PayrollItemWageRef", "Notes",
        "BillableStatus", "IsBillable", "ExternalGUID"
    ]

    class Meta:
        name = "TimeTrackingAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
            "required": True,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
            "type": "Element",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class TimeTrackingMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "EntityRef",
        "CustomerRef", "ItemServiceRef", "Duration", "ClassRef",
        "PayrollItemWageRef", "Notes", "BillableStatus"
    ]

    class Meta:
        name = "TimeTrackingMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
            "required": True,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
            "type": "Element",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )


@dataclass
class TimeTracking(QBMixinWithSave):
    class Meta:
        name = "TimeTracking"
        plural_class_name = "TimeTrackings"

    Query: Type[TimeTrackingQuery] = TimeTrackingQuery
    Add: Type[TimeTrackingAdd] = TimeTrackingAdd
    Mod: Type[TimeTrackingMod] = TimeTrackingMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
            "type": "Element",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class TimeTrackings(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "TimeTracking"
        plural_of = TimeTracking

    def __init__(self):
        super().__init__()


@dataclass
class TransactionModifiedDateRangeFilter(QBMixin):
    FIELD_ORDER = [
        "FromModifiedDate", "ToModifiedDate", "DateMacro"
    ]

    class Meta:
        name = "TransactionModifiedDateRangeFilter"

    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )


@dataclass
class TransactionDateRangeFilter(QBMixin):
    FIELD_ORDER = [
        "FromTxnDate", "ToTxnDate", "DateMacro"
    ]

    class Meta:
        name = "TransactionDateRangeFilter"

    from_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromTxnDate",
            "type": "Element",
        },
    )
    to_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToTxnDate",
            "type": "Element",
        },
    )
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )


@dataclass
class TransactionEntityFilter(QBMixin):
    FIELD_ORDER = [
        "EntityTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionEntityFilter"

    entity_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "EntityTypeFilter",
            "type": "Element",
            "valid_values": ["Customer", "Employee", "OtherName", "Vendor"]
        },
    )
    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
            "max_length": 36,
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionAccountFilter(QBMixin):
    FIELD_ORDER = [
        "AccountTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionAccountFilter"

    account_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountTypeFilter",
            "type": "Element",
            "valid_values": [
                "AccountsPayable", "AccountsReceivable", "AllowedFor1099", "APAndSalesTax",
                "APOrCreditCard", "ARAndAP", "Asset", "BalanceSheet", "Bank",
                "BankAndARAndAPAndUF", "BankAndUF", "CostOfSales", "CreditCard",
                "CurrentAsset", "CurrentAssetAndExpense", "CurrentLiability", "Equity",
                "EquityAndIncomeAndExpense", "ExpenseAndOtherExpense", "FixedAsset",
                "IncomeAndExpense", "IncomeAndOtherIncome", "Liability", "LiabilityAndEquity",
                "LongTermLiability", "NonPosting", "OrdinaryExpense", "OrdinaryIncome",
                "OrdinaryIncomeAndCOGS", "OrdinaryIncomeAndExpense", "OtherAsset",
                "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense",
                "OtherIncome", "OtherIncomeOrExpense"
            ],
        },
    )
    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
            "max_length": 36,
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionItemFilter(QBMixin):
    FIELD_ORDER = [
        "ItemTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionItemFilter"

    item_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemTypeFilter",
            "type": "Element",
            "valid_values": [
                "AllExceptFixedAsset", "Assembly", "Discount", "FixedAsset", "Inventory",
                "InventoryAndAssembly", "NonInventory", "OtherCharge", "Payment",
                "Sales", "SalesTax", "Service"
            ]
        },
    )
    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionClassFilter(QBMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionClassFilter"

    list_ids: List[str] = list_ids
    full_names: List[str] = full_names
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class CurrencyFilter(QBMixin):
    FIELD_ORDER = [
        "ListID", "FullName"
    ]

    class Meta:
        name = "CurrencyFilter"

    list_ids: List[str] = list_ids
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 64,
        },
    )


@dataclass
class TransactionQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "RefNumber", "RefNumberCaseSensitive",
        "RefNumberFilter", "RefNumberRangeFilter", "TransactionModifiedDateRangeFilter",
        "TransactionDateRangeFilter", "TransactionEntityFilter",
        "TransactionAccountFilter", "TransactionItemFilter", "TransactionClassFilter",
        "TransactionTypeFilter", "TransactionDetailLevelFilter",
        "TransactionPostingStatusFilter", "TransactionPaidStatusFilter",
        "CurrencyFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "TransactionQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    transaction_modified_date_range_filter: Optional[
        TransactionModifiedDateRangeFilter
    ] = field(
        default=None,
        metadata={
            "name": "TransactionModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    transaction_date_range_filter: Optional[TransactionDateRangeFilter] = (
        field(
            default=None,
            metadata={
                "name": "TransactionDateRangeFilter",
                "type": "Element",
            },
        )
    )
    transaction_entity_filter: Optional[TransactionEntityFilter] = field(
        default=None,
        metadata={
            "name": "TransactionEntityFilter",
            "type": "Element",
        },
    )
    transaction_account_filter: Optional[TransactionAccountFilter] = field(
        default=None,
        metadata={
            "name": "TransactionAccountFilter",
            "type": "Element",
        },
    )
    transaction_item_filter: Optional[TransactionItemFilter] = field(
        default=None,
        metadata={
            "name": "TransactionItemFilter",
            "type": "Element",
        },
    )
    transaction_class_filter: Optional[TransactionClassFilter] = field(
        default=None,
        metadata={
            "name": "TransactionClassFilter",
            "type": "Element",
        },
    )
    transaction_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionTypeFilter",
            "type": "Element",
            "valid_values": [
                "All", "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
                "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit",
                "YTDAdjustment"
            ],
        },
    )
    transaction_detail_level_filter: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "TransactionDetailLevelFilter",
                "type": "Element",
                "valid_values": [
                    "All", "SummaryOnly", "AllExceptSummary"
                ],
            },
        )
    )
    transaction_posting_status_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionPostingStatusFilter",
            "type": "Element",
            "valid_values": [
                "All", "SummaryOnly", "AllExceptSummary"
            ],
        },
    )
    transaction_paid_status_filter: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "TransactionPaidStatusFilter",
                "type": "Element",
                "valid_values": [
                    "Either", "Closed", "Open"
                ],
            },
        )
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class Transaction(QBMixinWithSave):

    class Meta:
        name = "Transaction"
        plural_class_name = "Transactions"

    Query: Type[TransactionQuery] = TransactionQuery
    #No Add
    #No Mod

    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
                "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit",
                "YTDAdjustment"
            ],
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class Transactions(PluralMixin):

    class Meta:
        name = "Transaction"
        plural_of = Transaction

    def __init__(self):
        super().__init__()


@dataclass
class TransferQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "TransferQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class TransferAdd(QBAddRqMixin):
    FIELD_ORDER = [
        "TxnDate", "TransferFromAccountRef", "TransferToAccountRef",
        "ClassRef", "Amount", "Memo"
    ]

    class Meta:
        name = "TransferAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class TransferMod(QBModRqMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "TransferFromAccountRef",
        "TransferToAccountRef", "ClassRef", "Amount", "Memo"
    ]

    class Meta:
        name = "TransferMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class Transfer(QBMixinWithSave):
    class Meta:
        name = "Transfer"
        plural_class_name = "Transfers"

    Query: Type[TransferQuery] = TransferQuery
    Add: Type[TransferAdd] = TransferAdd
    Mod: Type[TransferMod] = TransferMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    from_account_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FromAccountBalance",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
            "type": "Element",
        },
    )
    to_account_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ToAccountBalance",
            "type": "Element",
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = amount
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class Transfers(PluralMixin, PluralTrxnSaveMixin):
    class Meta:
        name = "Transfer"
        plural_of = Transfer

    def __init__(self):
        super().__init__()


@dataclass
class TxnDel(QBMixin):
    FIELD_ORDER = [
        "TxnDelType", "TxnID"
    ]

    class Meta:
        name = "TxnDel"

    txn_del_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDelType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "TimeTracking", "TransferInventory",
                "VehicleMileage", "VendorCredit"
            ],
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class TxnVoid(QBMixin):
    FIELD_ORDER = [
        "TxnVoidType", "TxnID"
    ]

    class Meta:
        name = "TxnVoid"

    txn_void_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnVoidType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo",
                "Deposit", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
                "SalesReceipt", "VendorCredit"
            ],
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )

# endregion
