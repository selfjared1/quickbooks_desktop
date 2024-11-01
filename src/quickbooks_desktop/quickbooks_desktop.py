import win32com.client, re, json, threading, time, logging, easygui
from lxml import etree as et
import xml.etree.ElementTree as ETree
from dataclasses import dataclass, field, fields, is_dataclass, MISSING
from typing import Optional, Union, Dict, Type, Any, get_origin, get_args, List
import datetime as dt
from dateutil import parser
from datetime import timedelta, datetime
import tkinter as tk
from PIL import Image, ImageTk
from decimal import Decimal


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# region Common Lists and Dicts


yes_no_dict = {'Yes': True, 'yes': True, 'No': False, 'no': False}

VALID_TXN_DATA_EXT_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
    "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
    "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
    "ItemReceipt", "JournalEntry", "PurchaseOrder", "ReceivePayment",
    "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck", "VendorCredit"
]

VALID_LIST_DATA_EXT_TYPE_VALUES = ["Account", "Customer", "Employee", "Item", "OtherName", "Vendor"]

VALID_TXN_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard", "BuildAssembly",
    "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo", "Deposit",
    "Estimate", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
    "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck", "PurchaseOrder",
    "ReceivePayment", "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck",
    "Transfer", "VendorCredit", "YTDAdjustment"
]

VALID_OPERATOR_VALUES = ["LessThan", "LessThanEqual", "Equal", "GreaterThan", "GreaterThanEqual"]

VALID_RELATION_VALUES = [
        "Spouse", "Partner", "Mother", "Father", "Sister", "Brother",
        "Son", "Daughter", "Friend", "Other"
    ]

VALID_ACCOUNT_TYPE_VALUES = [
    "AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold", "CreditCard",
    "Equity", "Expense", "FixedAsset", "Income", "LongTermLiability", "NonPosting",
    "OtherAsset", "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense", "OtherIncome"
]

VALID_DETAIL_ACCOUNT_TYPE_VALUES = [
    "AP", "AR", "AccumulatedAdjustment", "AccumulatedAmortization", "AccumulatedAmortizationOfOtherAssets",
    "AccumulatedDepletion", "AccumulatedDepreciation", "AdvertisingOrPromotional", "AllowanceForBadDebts",
    "Amortization", "Auto", "BadDebts", "BankCharges", "Buildings", "CashOnHand", "CharitableContributions",
    "Checking", "CommonStock", "CostOfLabor", "CostOfLaborCOS", "CreditCard", "DepletableAssets",
    "Depreciation", "DevelopmentCosts", "DiscountsOrRefundsGiven", "DividendIncome", "DuesAndSubscriptions",
    "EmployeeCashAdvances", "Entertainment", "EntertainmentMeals", "EquipmentRental", "EquipmentRentalCOS",
    "FederalIncomeTaxPayable", "FurnitureAndFixtures", "Goodwill", "Insurance", "InsurancePayable",
    "IntangibleAssets", "InterestEarned", "InterestPaid", "Inventory", "InvestmentMortgageOrRealEstateLoans",
    "InvestmentOther", "InvestmentTaxExemptSecurities", "InvestmentUSGovObligations", "Land", "LeaseBuyout",
    "LeaseholdImprovements", "LegalAndProfessionalFees", "Licenses", "LineOfCredit", "LoanPayable",
    "LoansToOfficers", "LoansToOthers", "LoansToStockholders", "MachineryAndEquipment", "MoneyMarket",
    "NonProfitIncome", "NotesPayable", "OfficeOrGeneralAdministrativeExpenses", "OpeningBalanceEquity",
    "OrganizationalCosts", "OtherCostsOfServiceCOS", "OtherCurrentAssets", "OtherCurrentLiab",
    "OtherFixedAssets", "OtherInvestmentIncome", "OtherLongTermAssets", "OtherLongTermLiab", "OtherMiscExpense",
    "OtherMiscIncome", "OtherMiscServiceCost", "OtherPrimaryIncome", "OwnersEquity", "PaidInCapitalOrSurplus",
    "PartnerContributions", "PartnerDistributions", "PartnersEquity", "PayrollClearing", "PayrollExpenses",
    "PayrollTaxPayable", "PenaltiesAndSettlements", "PreferredStock", "PrepaidExpenses", "PrepaidExpensesPayable",
    "PromotionalMeals", "RentOrLeaseOfBuildings", "RentsHeldInTrust", "RentsInTrustLiab", "RepairAndMaintenance",
    "Retainage", "RetainedEarnings", "SalesOfProductIncome", "SalesTaxPayable", "Savings", "SecurityDeposits",
    "ServiceOrFeeIncome", "ShareholderNotesPayable", "ShippingFreightAndDelivery", "ShippingFreightAndDeliveryCOS",
    "StateOrLocalIncomeTaxPayable", "SuppliesAndMaterials", "SuppliesAndMaterialsCOGS", "TaxExemptInterest",
    "TaxesPaid", "Travel", "TravelMeals", "TreasuryStock", "TrustAccounts", "TrustAccountsLiab",
    "UndepositedFunds", "Utilities", "Vehicles"
]

VALID_SPECIAL_ACCOUNT_TYPE_VALUES = [
    "AccountsPayable", "AccountsReceivable", "CondenseItemAdjustmentExpenses", "CostOfGoodsSold",
    "DirectDepositLiabilities", "Estimates", "ExchangeGainLoss", "InventoryAssets", "ItemReceiptAccount",
    "OpeningBalanceEquity", "PayrollExpenses", "PayrollLiabilities", "PettyCash", "PurchaseOrders",
    "ReconciliationDifferences", "RetainedEarnings", "SalesOrders", "SalesTaxPayable", "UncategorizedExpenses",
    "UncategorizedIncome", "UndepositedFunds"
]

VALID_CASH_FLOW_CLASSIFICATION_VALUES = ["None", "Operating", "Investing", "Financing", "NotApplicable"]


# endregion


# region Fields


@dataclass
class QBDates:
    _name = 'QBDates'
    date: Optional[Union[str, dt.date, dt.datetime]] = field(default=None)
    date_is_macro: bool = field(init=False, default=False)

    # def __post_init__(self):
    #     self.date = self.date  # Trigger the setter for initial date value

    @property
    def macro_dict(self):
        return self.get_macro_dict()

    @property
    def date(self) -> Optional[Union[str, dt.date, dt.datetime]]:
        return self._date

    @date.setter
    def date(self, value: Optional[Union[str, dt.date, dt.datetime]]):
        if value is None:
            raise ValueError("You did not include a date")
        else:
            self._date = self.parse_date(value)

    def parse_date(self, date: Union[str, dt.date, dt.datetime]) -> str:
        if isinstance(date, str):
            if date.lower() in self.macro_dict:
                self.date_is_macro = True
                return str(self.macro_dict[date.lower()])
            else:
                try:
                    date_parsed = parser.parse(date)
                    return date_parsed
                except Exception as e:
                    raise ValueError(f'Your date parameter "{date}" could not be parsed: {e}')
        elif isinstance(date, dt.datetime):
            return date
        elif isinstance(date, dt.date):
            return date
        else:
            raise ValueError(f'Unsupported date type: {type(date)}')

    @staticmethod
    def get_macro_dict() -> Dict[str, int]:
        return {
            "rdmall": 0,
            "rdmtoday": 1,
            "rdmthisweek": 2,
            "rdmthisweektodate": 3,
            "rdmthismonth": 4,
            "rdmthismonthtodate": 5,
            "rdmthisquarter": 6,
            "rdmthisquartertodate": 7,
            "rdmthisyear": 8,
            "rdmthisyeartodate": 9,
            "rdmyesterday": 10,
            "rdmlastweek": 11,
            "rdmlastweektodate": 12,
            "rdmlastmonth": 13,
            "rdmlastmonthtodate": 14,
            "rdmlastquarter": 15,
            "rdmlastquartertodate": 16,
            "rdmlastyear": 17,
            "rdmlastyearTodate": 18,
            "rdmnextweek": 19,
            "rdmnextfourweeks": 20,
            "rdmnextmonth": 21,
            "rdmnextquarter": 22,
            "rdmnextyear": 23,
            "all": 0,
            "today": 1,
            "this_week": 2,
            "this_week_to_date": 3,
            "this_month": 4,
            "this_month_to_date": 5,
            "this_quarter": 6,
            "this_quarter_to_date": 7,
            "this_year": 8,
            "this_year_to_date": 9,
            "yesterday": 10,
            "last_week": 11,
            "last_week_to_date": 12,
            "last_month": 13,
            "last_month_to_date": 14,
            "last_quarter": 15,
            "last_quarter_to_date": 16,
            "last_year": 17,
            "last_year_to_date": 18,
            "next_week": 19,
            "next_four_weeks": 20,
            "next_month": 21,
            "next_quarter": 22,
            "next_year": 23,
        }

    def __str__(self):
        if isinstance(self._date, int):  # Macro values are stored as integers
            return str(self._date)
        elif isinstance(self._date, str):
            return self._date
        else:
            return self._date.strftime("%Y-%m-%d")

    def to_xml(self, field_name):
        element = et.Element(snake_to_camel(field_name))
        element.text = self.__str__()
        return element


    @classmethod
    def from_xml(cls, xml_element):
        qb_date = cls(xml_element.text)
        return qb_date


@dataclass
class QBDateTime:
    _name = 'QBDateTime'
    datetime_value: Optional[Union[str, datetime]] = field(default=None)

    @property
    def datetime_value(self) -> Optional[Union[str, datetime]]:
        return self._datetime_value

    @datetime_value.setter
    def datetime_value(self, value: Optional[Union[str, datetime]]):
        if value is None:
            raise ValueError("You did not include a datetime value")
        else:
            self._datetime_value = self.parse_datetime(value)

    def parse_datetime(self, datetime_str: Union[str, datetime]) -> datetime:
        if isinstance(datetime_str, str):
            try:
                # Parse datetime string in ISO 8601 format
                return parser.isoparse(datetime_str)
            except Exception as e:
                raise ValueError(f'Your datetime parameter "{datetime_str}" could not be parsed: {e}')
        elif isinstance(datetime_str, datetime):
            return datetime_str
        else:
            raise ValueError(f'Unsupported datetime type: {type(datetime_str)}')

    def __str__(self):
        if isinstance(self._datetime_value, datetime):
            # Format as ISO 8601 string
            return self._datetime_value.isoformat()
        return str(self._datetime_value)

    def to_xml(self, field_name: str) -> et.Element:
        element = et.Element(field_name)
        element.text = self.__str__()
        return element

    @classmethod
    def from_xml(cls, xml_element: et.Element) -> 'QBDateTime':
        datetime_str = xml_element.text
        return cls(datetime_str)


@dataclass
class QBTime:
    def __init__(self, duration: timedelta):
        self.duration = duration
        self.value = self._convert_to_qb_format(duration)

    @staticmethod
    def is_valid_xml_format(duration_str):
        if isinstance(duration_str, str):
            pattern = r"([+\-]?)PT((\d+)H)?((\d+)M)?((\d+)S)?"
            return bool(re.fullmatch(pattern, duration_str))
        else:
            return False

    @staticmethod
    def is_valid_time_format(duration_str):
        if isinstance(duration_str, str):
            pattern = r"^\d{2}:\d{2}(:\d{2})?$"
            return bool(re.fullmatch(pattern, duration_str))
        else:
            return False

    @staticmethod
    def _convert_to_qb_format(duration: timedelta) -> str:
        if isinstance(duration, str) and str(duration).isnumeric():
            parts = duration.split('.')
            hours = int(parts[0])
            minutes = int(parts[1])
            duration = timedelta(hours=hours, minutes=minutes)
        elif isinstance(duration, str) and QBTime.is_valid_xml_format(duration):
            return duration
        elif QBTime.is_valid_xml_format(duration):
            time = QBTime.from_hhmm_format(duration)
            duration = time.value
        else:
            pass

        total_seconds = int(duration.total_seconds())
        sign = '-' if total_seconds < 0 else ''
        total_seconds = abs(total_seconds)

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        duration_str = f"{sign}PT"
        if hours > 0:
            duration_str += f"{hours}H"
        if minutes > 0:
            duration_str += f"{minutes}M"
        if seconds > 0:
            duration_str += f"{seconds}S"

        return duration_str

    @classmethod
    def from_qb_format(cls, duration_str: str) -> 'QBTime':
        pattern = r"([+\-]?)PT((\d+)H)?((\d+)M)?((\d+)S)?"
        match = re.fullmatch(pattern, duration_str)
        if not match:
            raise ValueError(f"Invalid QuickBooks duration format: {duration_str}")

        sign = -1 if match.group(1) == '-' else 1
        hours = int(match.group(3)) if match.group(3) else 0
        minutes = int(match.group(5)) if match.group(5) else 0
        seconds = int(match.group(7)) if match.group(7) else 0

        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds) * sign
        return cls(duration)

    @classmethod
    def from_hhmm_format(cls, time_str: str) -> 'QBTime':
        """Convert a time string in HH:MM or HH:MM:SS format to a QBTime object."""
        try:
            parts = time_str.split(':')
            if len(parts) == 2:
                hours, minutes = map(int, parts)
                seconds = 0
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
            else:
                raise ValueError
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            return cls(duration)
        except ValueError:
            raise ValueError(f"Invalid HH:MM or HH:MM:SS format: {time_str}")

    @classmethod
    def parse(cls, time_str: str) -> 'QBTime':
        """Convert a time string in either QuickBooks or HH:MM or HH:MM:SS format to a QBTime object."""
        if time_str.startswith("PT") or time_str.startswith("-PT"):
            return cls.from_qb_format(time_str)
        elif re.match(r"^\d+:\d{2}(:\d{2})?$", time_str):
            return cls.from_hhmm_format(time_str)
        else:
            raise ValueError(f"Invalid time format: {time_str}")

    @classmethod
    def from_float_hours(cls, hours_float):
        hours = int(hours_float)
        minutes = int((hours_float - hours) * 60)
        time_delta = timedelta(hours=hours, minutes=minutes)
        qb_time = cls(time_delta)
        return qb_time

    @classmethod
    def from_xml(cls, element: et.Element) -> 'QBTime':
        duration_str = element.text.strip()
        return cls.from_qb_format(duration_str)

    def to_xml(self, field_name) -> et.Element:
        element = et.Element(snake_to_camel(field_name))
        element.text = self._convert_to_qb_format(self.value)
        return element

    def to_float_hours(self):
        total_minutes = int(self.duration.total_seconds() / 60)
        return total_minutes / 60

    def __str__(self):
        return self._convert_to_qb_format(self.value)


@dataclass
class QBPriceType(str):
    def __new__(cls, value):
        return super().__new__(cls, value)

    @staticmethod
    def _validate_price(value) -> None:
        pattern = r"([+\-]?[0-9]{1,10}(\.[0-9]{1,5})?)?"
        if value is not None and not re.fullmatch(pattern, value):
            raise ValueError(
                f"Invalid price: {value}. Must be a number with up to 10 digits before the decimal and up to 5 digits after. "
                f"Examples of valid values: '12345', '-12345', '12345.6789', '-0.12345', '+0.12345'."
            )

    @classmethod
    def from_xml(cls, element: et.Element) -> 'QBPriceType':
        price_str = element.text.strip()
        return cls(price_str)

    def to_xml(self) -> et.Element:
        self._validate_price(self)
        element = et.Element("QuickBooksPrice")
        element.text = str(self)
        return element


# endregion


# region Connection To Desktop And Utilities

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
                logger.debug(date_str)
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError as e:
                logger.debug(f"Error parsing date: {e}")
                raise
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
        logger.debug(f"Error parsing float: {e}")
        raise


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


class SearchableComboBox():
    def __init__(self, root, options, geometry) -> None:
        self.dropdown_id = None
        self.options = options
        self.geometry = geometry

        # Create a Text widget for the entry field
        wrapper = tk.Frame(root)
        wrapper.pack()

        self.entry = tk.Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.pack(side=tk.LEFT)

        # Dropdown icon/button
        self.icon = ImageTk.PhotoImage(Image.open("dropdown_arrow.png").resize((16,16)))
        tk.Button(wrapper, image=self.icon, command=self.show_dropdown).pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(root, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        if not typed_value:
            # If the entry is empty, display all options
            self.listbox.delete(0, tk.END)
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            # Filter options based on the typed value
            self.listbox.delete(0, tk.END)
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()

def convert_integer(value):
    if isinstance(value, int):
        if value == 1:
            return 'True'
        elif value == 0:
            return 'False'
        else:
            return str(value)
    return value

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
    def __parse_list_field_type(init_args, field, field_type, xml_elements):
        # if the field type is a list
        for xml_element in xml_elements:
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

        if getattr(instance, 'validate', False):
            instance.validate()
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


class QBMixin(MaxLengthMixin, ToXmlMixin, FromXmlMixin, ValidationMixin, ReprMixin, SaveMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


class QBMixinWithQuery(QBMixin):

    # class Query(QBQueryMixin):
    #     pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Query.set_name(cls.Meta.name)


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
                plural_instance._items.append(plural_of_instance)
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

    @classmethod
    def update_db(cls, qb, session):
        qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
        plural_instance = cls.__get_last_time_modified(qb_max_time_modified, qb)
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

    def to_xml_file(self, file_path: str) -> None:
        """
        Generates an XML file with the plural objects.
        Creates a root element based on the Meta class name, appends all items, and writes to the file path.

        Args:
            file_path (str): The path of the file to write the XML to. The file will be replaced if it exists.
        """
        # Convert each child to an XML element
        list_of_xml = self.to_xml()

        # Create the root element using the Meta class name
        root = et.Element(f"{self.Meta.name}QueryRs")

        # Append each child XML element to the root
        for xml_element in list_of_xml:
            root.append(xml_element)

        # Convert the root element to a formatted XML string
        xml_str = et.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

        # Write the XML string to the specified file path, replacing the file if it exists
        with open(file_path, "w") as file:
            file.write(xml_str)

        logger.debug('Finished to_xml_file')


class PluralListSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for item in self:
            if item.list_id is not None:
                mod_xml = item._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = item._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

class PluralTrxnSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for trxn in self:
            if trxn.trxn_id is not None:
                mod_xml = trxn._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = trxn._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

    def add_all(self, qb):
        xml_requests = []
        for trxn in self:
            add_xml = trxn._get_add_rq_xml()
            xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

    def set_ids_to_none(self, id_name):
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

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
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


    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
class DataExtAdd(QBAddMixin):
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
            "valid_values": ["Account", "Customer", "Employee", "Item", "OtherName", "Vendor"]
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
class DataExtMod(QBAddMixin):
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
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES + VALID_LIST_DATA_EXT_TYPE_VALUES + ["Company"],
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
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
        },
    )

@dataclass
class AccountFilter(ToXmlMixin):

    class Meta:
        name = "AccountFilter"

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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
class ExpenseLineAdd(QBMixin):
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
class ItemLineAdd(QBMixin):
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
class ItemGroupLineAdd(QBMixin):
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
class ExpenseLineMod(QBMixin):
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
class ItemLineMod(QBMixin):
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
class ItemGroupLineMod(QBMixin):
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
class ExpenseLine(QBMixin):

    class Meta:
        name = "ExpenseLine"

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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemLine(QBMixin):

    class Meta:
        name = "ItemLine"

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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemGroupLine(QBMixin):

    class Meta:
        name = "ItemGroupLine"

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
    item_line_ret: List[ItemLine] = field(
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
class DiscountLineAdd(QBMixin):

    class Meta:
        name = "DiscountLineAdd"

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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
class DiscountLine(QBMixin):

    class Meta:
        name = "DiscountLine"

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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
class ItemGroupLine(QBMixin):

    class Meta:
        name = "ItemGroupLine"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
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


@dataclass
class ItemInventoryAssemblyLine(QBMixin):

    class Meta:
        name = "ItemInventoryAssemblyLine"

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
        "include_ret_element", "owner_id", "request_id"
    ]

    class Meta:
        name = "AccountQuery"

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
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


@dataclass
class AccountAdd(AccountBase, QBAddMixin):
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
class SpecialAccountAdd(QBAddMixin):
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
class AccountMod(AccountBase, QBModMixin):
    FIELD_ORDER = [
        "list_id", "edit_sequence", "name", "is_active", "parent_ref",
        "account_type", "account_number", "bank_number", "desc",
        "open_balance", "open_balance_date", "tax_line_id",
        "currency_ref", "include_ret_element"
    ]

    class Meta:
        name = "AccountMod"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class Account(AccountBase, QBMixinWithQuery):
    class Meta:
        name = "Account"

    Query: Type[AccountQuery] = AccountQuery
    Add: Type[AccountAdd] = AccountAdd
    SpecialAccountAdd: Type[SpecialAccountAdd] = SpecialAccountAdd
    Mod: Type[AccountMod] = AccountMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159,
        },
    )
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

    data_ext_ret: List[DataExt] = field(
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
class BillingRateAdd(QBAddMixin):
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

    Query: Type[BillingRateQuery] = BillingRateQuery
    Add: Type[BillingRateAdd] = BillingRateAdd
    # there is no Mod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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


@dataclass
class ClassInQBQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "ClassQuery"

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    meta_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaData",
            "type": "Attribute",
            "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
        },
    )


@dataclass
class ClassInQBAdd(QBAddMixin):
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
class ClassInQBMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "ClassMod"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
class ClassInQB(QBMixinWithQuery):
    class Meta:
        name = "Class"

    Query: Type[ClassInQBQuery] = ClassInQBQuery
    Add: Type[ClassInQBAdd] = ClassInQBAdd
    Mod: Type[ClassInQBMod] = ClassInQBMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    # meta_data: CurrencyQueryRqTypeMetaData = field(
    #     default=CurrencyQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )


@dataclass
class CurrencyAdd(QBAddMixin):
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
class CurrencyMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "CurrencyCode",
        "CurrencyFormat"
    ]

    class Meta:
        name = "CurrencyMod"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
class Currency(QBMixinWithQuery):
    class Meta:
        name = "Currency"

    Query: Type[CurrencyQuery] = CurrencyQuery
    Add: Type[CurrencyAdd] = CurrencyAdd
    Mod: Type[CurrencyMod] = CurrencyMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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


@dataclass
class CustomerMsgQuery(QBQueryMixin):

    class Meta:
        name = "CustomerMsgQuery"

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    meta_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaData",
            "type": "Attribute",
            "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"]
        },
    )


@dataclass
class CustomerMsgAdd(QBAddMixin):

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
class CustomerMsg(QBMixinWithQuery):

    class Meta:
        name = "CustomerMsg"

    Query: Type[CustomerMsgQuery] = CustomerMsgQuery
    Add: Type[CustomerMsgAdd] = CustomerMsgAdd
    #There is no Mod


    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    #todo: Add Field
    # meta_data: CustomerQueryRqTypeMetaData = field(
    #     default=CustomerQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )
    # iterator: Optional[CustomerQueryRqTypeIterator] = field(
    #     default=None,
    #     metadata={
    #         "type": "Attribute",
    #     },
    # )
    # iterator_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "iteratorID",
    #         "type": "Attribute",
    #     },
    # )

@dataclass
class CustomerAdd(QBAddMixin):
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
class CustomerMod(QBModMixin):
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

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
class Customer(QBMixinWithQuery):
    class Meta:
        name = "Customer"

    Query: Type[CustomerQuery] = CustomerQuery
    Add: Type[CustomerAdd] = CustomerAdd
    Mod: Type[CustomerMod] = CustomerMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
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
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 209
        },
    )
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
    data_ext_ret: List[DataExt] = field(
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class Employee(QBMixinWithQuery):
    class Meta:
        name = "Employee"

    class Query(EmployeeQuery):
        pass


    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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
    #todo: Add Field
    # external_guid: Optional[ExternalGuid] = field(
    #     default=None,
    #     metadata={
    #         "name": "ExternalGUID",
    #         "type": "Element",
    #     },
    # )
    # data_ext_ret: List[DataExtRet] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExtRet",
    #         "type": "Element",
    #     },
    # )

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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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


@dataclass
class InventorySiteAdd(QBAddMixin):
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
class InventorySiteMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentSiteRef", "SiteDesc",
        "Contact", "Phone", "Fax", "Email", "SiteAddress", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteMod"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
class InventorySite(QBMixinWithQuery):

    class Meta:
        name = "InventorySite"

    Query: Type[InventorySiteQuery] = InventorySiteQuery
    Add: Type[InventorySiteAdd] = InventorySiteAdd
    Mod: Type[InventorySiteMod] = InventorySiteMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
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
class ItemAddMixin(QBAddMixin):
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
class ItemModMixin(QBModMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
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
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159,
        },
    )
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
def ItemWithClassAndTaxMixin(ItemMixin):


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
class ItemDiscount(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemDiscount"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemGroup(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemGroup"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemInventory(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemInventory"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemInventoryAssembly(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemInventoryAssembly"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemNonInventory(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemNonInventory"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemOtherCharge(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemOtherCharge"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemPayment(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemPayment"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemSalesTax(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSalesTax"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemSalesTaxGroup(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSalesTaxGroup"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemService(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemService"

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
    data_ext_ret: List[DataExt] = field(
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


@dataclass
class ItemSubtotal(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSubtotal"

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
    data_ext_ret: List[DataExt] = field(
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


# endregion
