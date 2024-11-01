import win32com.client
from lxml import etree as et
import xml.etree.ElementTree as ETree
import logging
import easygui

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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

    def _prepare_request(self, requestXML):
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

        return QBXML


    def send_xml(self, requestXML, encoding="utf-8"):
        """
        This method
            1. finishes the XML build
            2. ensures the XML request has key components
            3. sends the request to QuickBooks
        :param requestXML: The request element under the QBXMLMsgsRq tag.
        :return: responseXML from the quickbooks processor
        """

        QBXML = self._prepare_request(requestXML)

        declaration = f"""<?xml version="1.0" encoding="{encoding}"?><?qbxml version="{self.SDK_version}"?>"""
        full_request = declaration + et.tostring(QBXML, encoding=encoding).decode(encoding)
        logger.debug(f'full_request to go to qb: {full_request}')

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
            # Additional Things:
            QBXML = et.fromstring(responseXML)
            QBXMLMsgsRs = QBXML.find('QBXMLMsgsRs')
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

        if QBXMLMsgsRs is not None:
            responses = QBXMLMsgsRs.getchildren()
            # todo: parse into actual objects
            return responses
        else:
            logging.debug(f'responseXML = {responseXML}')
            return None

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