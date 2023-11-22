from datetime import timedelta, datetime
import re
import dateutil.parser as parser
import datetime as dt
import pandas as pd
from typing import Optional
import attr
from lxml import etree

data_type_translator_python_to_qb = {
    'float': 'AMTTYPE',
    'datetime': 'DATETIMETYPE',
    'int': 'INTTYPE',
    #todo: 'float': 'PERCENTTYPE',
    #todo: 'float': 'PRICETYPE',
    #todo: 'float': 'QUANTYPE',
    'str': 'STR1024TYPE',
    #todo: 'float': 'STR255TYPE'
}

data_type_translator_qb_to_python = {
    'AMTTYPE': 'float',
    'DATETIMETYPE': 'datetime',
    'INTTYPE': 'int',
    'PERCENTTYPE': 'float',
    'PRICETYPE': 'float',
    'QUANTYPE': 'float',
    'STR1024TYPE': 'str',
    'STR255TYPE': 'float'
}

@attr.s(auto_attribs=True)
class Ref:
    ref_label: Optional[str] = None
    id_name: Optional[str] = None
    ID: Optional[str] = None
    name_name: Optional[str] = None
    Name: Optional[str] = None

    def to_xml(self):
        root = etree.Element(self.ref_label)
        if self.id_name and self.ID is not None:
            id_elem = etree.Element(self.id_name)
            id_elem.text = str(self.ID)
            root.append(id_elem)

        if self.name_name and self.Name is not None:
            name_elem = etree.Element(self.name_name)
            name_elem.text = str(self.Name)
            root.append(name_elem)
        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
        return xml_str

@attr.s(auto_attribs=True)
class DataExtRet:
    OwnerID: Optional[str] = None
    DataExtName: Optional[str] = None
    DataExtType: Optional[str] = None
    DataExtValue: Optional[str] = None

    @property
    def DataExtType(self):
        return self._DataExtType

    @DataExtType.setter
    def DataExtType(self, value):
        if value in data_type_translator_qb_to_python.keys():
            self._DataExtType = value
        elif value is None:
            self._DataExtType = None
        else:
            raise ValueError(f'The DataExtType is not a valid type.  The type provided was {value}. \n'
                             f'The acceptable types are AMTTYPE, DATETIMETYPE, INTTYPE, PERCENTTYPE, PRICETYPE, QUANTYPE, STR1024TYPE, and STR255TYPE.')

    @property
    def DataExtValue(self):
        return self._DataExtValue

    @DataExtValue.setter
    def DataExtValue(self, value):
        if self._DataExtType:
            if type(value) == data_type_translator_python_to_qb[type(value)]:
                self._DataExtValue = value
            else:
                raise ValueError(f'The DataExtValue is not the correct data type.  The value was {str(value)}. \n'
                                 f'The value type is {type(value)}. \n'
                                 f'The value type needs to be of python type {data_type_translator_qb_to_python[self._DataExtType]}')
        elif type(value) in data_type_translator_python_to_qb.keys():
            # todo: query DataExtRet to see what type it should be
            self._DataExtType = data_type_translator_python_to_qb[type(value)]
            self._DataExtValue = value
        else:
            raise ValueError(f'The DataExtValue is not the correct data type.  The value was {str(value)}. \n'
                                 f'The value type is {type(value)}. \n'
                                 f'The value type needs to be of python type {data_type_translator_qb_to_python[self._DataExtType]}')

class QBDateMacro:
    def __init__(self, date_macro=None):
        self.macro_dict = QBDateMacro.get_macro_dict(self)
        self.__macro_exception_message = f"""Your date_macro parameter "{date_macro}" could not be parsed.  \n
                            Try to use a QBDate object. \n
                            Or try one of the following Macro date strings: {self.macro_dict.keys()}"""
        self.date_macro = self.parse_date_macro(date_macro)
    def get_macro_dict(self):
        return {'rdmall': 0,
                'rdmtoday': 1,
                'rdmthisweek': 2,
                'rdmthisweektodate': 3,
                'rdmthismonth': 4,
                'rdmthismonthtodate': 5,
                'rdmthisquarter': 6,
                'rdmthisquartertodate': 7,
                'rdmthisyear': 8,
                'rdmthisyeartodate': 9,
                'rdmyesterday': 10,
                'rdmlastweek': 11,
                'rdmlastweektodate': 12,
                'rdmlastmonth': 13,
                'rdmlastmonthtodate': 14,
                'rdmlastquarter': 15,
                'rdmlastquartertodate': 16,
                'rdmlastyear': 17,
                'rdmlastyearTodate': 18,
                'rdmnextweek': 19,
                'rdmnextfourweeks': 20,
                'rdmnextmonth': 21,
                'rdmnextquarter': 22,
                'rdmnextyear': 23,
                'all': 0,
                'today': 1,
                'this_week': 2,
                'this_week_to_date': 3,
                'this_month': 4,
                'this_month_to_date': 5,
                'this_quarter': 6,
                'this_quarter_to_date': 7,
                'this_year': 8,
                'this_year_to_date': 9,
                'yesterday': 10,
                'last_week': 11,
                'last_week_to_date': 12,
                'last_month': 13,
                'last_month_to_date': 14,
                'last_quarter': 15,
                'last_quarter_to_date': 16,
                'last_year': 17,
                'last_year_to_date': 18,
                'next_week': 19,
                'next_four_weeks': 20,
                'next_month': 21,
                'next_quarter': 22,
                'next_year': 23}

    def parse_date_macro(self, date_macro):
        if date_macro is None:
            raise Exception(self.__macro_exception_message)
        elif isinstance(date_macro, str):
            if date_macro.lower() in self.macro_dict.keys():
                return self.macro_dict[date_macro.lower()]
            else:
                raise Exception(self.__macro_exception_message)
        elif isinstance(date_macro, int):
            if date_macro in self.macro_dict.values():
                return date_macro
            else:
                raise Exception(f"Please choose a number between 1 and 23. \n"
                                f"Or try one of the following Macro date strings: {self.macro_dict.keys()}")
        else:
            raise Exception(self.__macro_exception_message)

    def __str__(self):
        return str(self.date_macro)

class QBDate:
    def __init__(self, date=None):
        self.check_date_not_none(date)
        self.__date_exception_message = f"""Your date parameter "{date}" could not be parsed.  \n 
                                    Try to use a datetime object or a string in the format "mm/dd/yyyy". \n
                                    Or try using the QBDateMacro class."""
        self.date = self.parse_date(date)

    def check_date_not_none(self, date):
        if date is None:
            raise Exception('You did not include a date')

    def parse_date(self, date):
        if isinstance(date, str):
            try:
                date_parsed = parser.parse(date)
                date_obj = date_parsed.date()
                return date_obj
            except Exception as e:
                raise Exception(self.__date_exception_message)
        elif isinstance(date, dt.datetime):
            date_obj = date.date()
            return date_obj
        if isinstance(date, dt.date):
            return date
        elif pd.api.types.is_datetime64_any_dtype(date):
            date_obj = date.dt.date  # Extracts the date from a Pandas Series of datetime64 type
            return date_obj
        else:
            raise Exception(self.__date_exception_message)

    def __str__(self):
        return self.date.strftime("%m/%d/%Y")

    def to_xml(self):
        return self.__str__()

class QBTimeInterval:
    def __init__(self, input_data):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        if isinstance(input_data, str):
            if re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', input_data):
                self.sef_from_xml_format(input_data)
            elif re.match(r'\d{2}:\d{2}:\d{2}', input_data):  # Typical format: 'HH:MM:SS'
                self.set_from_string_format(input_data)
            else:
                raise ValueError("Invalid string format. Use 'PTnHnMnS' or 'HH:MM:SS'")
        elif isinstance(input_data, timedelta):
            self.set_from_timedelta(input_data)

    def sef_from_xml_format(self, time_str):
        match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', time_str)
        if match:
            self.hours = int(match.group(1)[:-1]) if match.group(1) else 0
            self.minutes = int(match.group(2)[:-1]) if match.group(2) else 0
            self.seconds = int(match.group(3)[:-1]) if match.group(3) else 0

    def set_from_string_format(self, time_str):
        time_parts = datetime.strptime(time_str, '%H:%M:%S').time()
        self.hours = time_parts.hour
        self.minutes = time_parts.minute
        self.seconds = time_parts.second

    def set_from_timedelta(self, timedelta_obj):
        total_seconds = int(timedelta_obj.total_seconds())
        self.hours = total_seconds // 3600
        self.minutes = (total_seconds % 3600) // 60
        self.seconds = total_seconds % 60

    def __str__(self):
        return f"PT{self.hours}H{self.minutes}M{self.seconds}S"