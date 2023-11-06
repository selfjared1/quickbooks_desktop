import win32com.client
from lxml import etree as et

class SessionManager():
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
        self.connection_open = False
        self.dispatch_str = "QBXMLRP2.RequestProcessor"
        self.qbXMLRP = None
        self.ticket = None
        self.SDK_version = SDK_version


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

    def send_xml(self, requestXML, keep_session_open=False, keep_connection_open=False):
        """
        This method
            1. finishes the XML build
            2. ensures the XML request has key components
            3. sends the request to QuickBooks
        :param requestXML: The request element under the QBXMLMsgsRq tag.
        :return: responseXML from the quickbooks processor
        """
        if self.qbXMLRP:
            self.qbXMLRP = self.dispatch()
            self.open_qb()
        elif not self.session_begun:
            self.begin_session()
            print('open session')
        root = et.Element("QBXML")
        QBXMLMsgsRq = et.SubElement(root, "QBXMLMsgsRq", onError="stopOnError")
        requestXML.attrib['requestID'] = "1"
        QBXMLMsgsRq.insert(1, requestXML)
        #todo: handle more than one request
        declaration = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="{self.SDK_version}"?>"""
        full_request = declaration + et.tostring(root, encoding='unicode')
        responseXML = self.qbXMLRP.ProcessRequest(self.ticket, full_request)
        if keep_session_open:
            return responseXML
        elif keep_connection_open:
            self.qbXMLRP.EndSession()
            return responseXML
        else:
            self.close_qb()
            return responseXML

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