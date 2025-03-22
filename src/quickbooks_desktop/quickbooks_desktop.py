import win32com.client
from src.quickbooks_desktop.qb_objects import *


class QuickbooksDesktop():
    """
    You'll need to run this in 32 Bit Python to work.
    QuickBooks Desktop session manager for XML.
    QuickBooks needs to be open and a company file open for this to work.
    The first time connecting you'll need to authorize the app inside of QuickBooks's UI.
    """

    def __init__(self, application_name="accountingpy", company_file=None, SDK_version='16.0'):
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
            self.qbXMLRP = win32com.client.Dispatch(self.dispatch_str)
        else:
            pass

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
            if not self.connection_open:
                self.open_connection()
            else:
                pass
            file_path = self.company_file if self.company_file else ""

            self.ticket = self.qbXMLRP.BeginSession(file_path, 0)
            self.session_begun = True

        except:
            try:
                file_path = self.company_file if self.company_file else ""
                self.ticket = self.qbXMLRP.BeginSession(file_path, 1)
                self.session_begun = True
            except Exception as e:
                raise(e)
                logger.debug(e)

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
            for element in requestXML:
                QBXMLMsgsRq.append(element)
        elif requestXML.tag == 'QBXML':
            QBXML = requestXML
            QBXMLMsgsRq = QBXML.find('QBXMLMsgsRq')
        elif requestXML.tag == 'QBXMLMsgsRq':
            QBXML = et.Element('QBXML')
            QBXML.append(requestXML)
            QBXMLMsgsRq = requestXML
        elif requestXML.tag[-2:] == 'Rq':
            QBXML = et.Element('QBXML')
            QBXMLMsgsRq = et.SubElement(QBXML, 'QBXMLMsgsRq', onError=self.on_error)
            QBXMLMsgsRq.append(requestXML)
        elif requestXML.tag[-5:] == 'Query':
            requestXML.tag = requestXML.tag + 'Rq'
            QBXML = et.Element('QBXML')
            QBXMLMsgsRq = et.SubElement(QBXML, 'QBXMLMsgsRq', onError=self.on_error)
            QBXMLMsgsRq.append(requestXML)
        else:
            # Neither QBXML nor QBXMLMsgsRq is the root, and the tag does not ends in Rq
            QBXML = et.Element('QBXML')
            QBXMLMsgsRq = et.SubElement(QBXML, 'QBXMLMsgsRq', onError=self.on_error)
            Rq = et.SubElement(QBXMLMsgsRq, requestXML.tag + 'Rq')
            Rq.append(requestXML)

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
        logger.debug('Begun _break_response_into_single_instances')
        instances = {}
        for response in responses:
            class_name = self._get_class_name_from_response_tag(response.tag)
            try:
                cls = globals().get(class_name)
                elements = response.getchildren()
                instance_list = []
                i = 0
                for element in elements:
                    # if i == 1376:
                    #     pass
                    if element.tag == 'ReportRet':
                        # In order to dynamically look for the correct class
                        element.tag = class_name +'Ret'
                    else:
                        pass
                    single_instance = cls.from_xml(element)
                    instance_list.append(single_instance)
                    i += 1
                    # print(i)
                instances[class_name] = instance_list
            except (ModuleNotFoundError, AttributeError) as e:
                logger.debug(f"Error loading class for {class_name}: {e}")
        logger.debug('Finished _break_response_into_single_instances')
        return instances

    def _break_response_into_plural_instances(self, responses):
        print('begin _break_response_into_plural_instances')
        instances = self._break_response_into_single_instances(responses)
        plural_instances = []
        for class_name, list_of_instances in instances.items():
            try:
                cls = globals().get(class_name)
                plural_cls = globals().get(cls.Meta.plural_class_name)
                print(f'creating plural_instance {class_name}')
                plural_instance = plural_cls.from_list(list_of_instances)
                print(f'Finished creating plural_instance {class_name}')
                if len(plural_instance):
                    plural_instances.append(plural_instance)
                else:
                    pass
            except Exception as e:
                print(f"Error loading class for {class_name}: {e}")
        print('end _break_response_into_plural_instances')
        return plural_instances

    def _create_full_request(self, requestXML, encoding="ISO-8859-1"):
        """
        Combines converting the request to lxml and ensuring the proper structure for the XML request.

        :param requestXML: The input request, which may be a string, xml.etree.ElementTree.Element,
                           lxml.etree.Element, or a list of these types.
        :return: A properly structured lxml.etree.Element for sending to QuickBooks.
        """
        requestXML = self._convert_to_lxml(requestXML)
        QBXML, QBXMLMsgsRq = self._ensure_qbxml_structure(requestXML)
        if isinstance(requestXML, list):
            i = 1
            for request in requestXML:
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

        xml_content = et.tostring(QBXML, encoding=encoding, pretty_print=False, method="xml").decode(encoding)
        over_escaped_pattern = re.compile(r'&amp;(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);')

        # Replace '&amp;' with '&' for matched patterns
        xml_content = over_escaped_pattern.sub(r'&\1;', xml_content)
        xml_content = xml_content.replace('–', '-') #Other characters

        if xml_content.startswith(f"<?xml version='1.0' encoding='{encoding}'?>"):
            full_request = xml_content.replace(
                f"<?xml version='1.0' encoding='{encoding}'?>",
                f'<?xml version="1.0" encoding="{encoding}"?><?qbxml version="16.0"?>',
                1
            )
        elif xml_content.startswith(f"""<?xml version="1.0" encoding="{encoding}"?>"""):
            full_request = xml_content.replace(
                f"""<?xml version="1.0" encoding="{encoding}"?>""",
                f'<?xml version="1.0" encoding="{encoding}"?><?qbxml version="16.0"?>',
                1
            )
        else:
            full_request = f"""<?xml version="1.0" encoding="{encoding}"?><?qbxml version="16.0"?>""" + xml_content

        #todo:
        # validate_qbxml(full_request, self.SDK_version)

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
                    'plural_list'
            'instances_dict' -> a dict with the key being the main class and the value being a list of initialized classes.
            'none' -> response won't be returned
        """

        if response_type == 'raw_str':
            return responseXML
        elif response_type == 'none':
            return None
        else:
            if '<?xml' in responseXML and 'encoding' in responseXML:
                responseXML = responseXML.encode('ISO-8859-1')
            else:
                pass
            QBXML = et.fromstring(responseXML)
            QBXMLMsgsRs = QBXML.find('QBXMLMsgsRs')
            logger.debug('QBXMLMsgsRs found')
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

    def send_xml(self, requestXML, encoding="ISO-8859-1", is_full_request=False, response_type='raw_str'):
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
            'plural_list' -> a list of plural class instances
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
            self.dispatch()
        else:
            pass

        if not self.connection_open:
            self.open_connection()
        else:
            pass

        if not self.session_begun:
            self.begin_session()
        else:
            pass

        logger.debug(f'Connection to QuickBooks is open')
        try:
            responseXML = self.qbXMLRP.ProcessRequest(self.ticket, full_request)
        except Exception as e:
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
