import re
from lxml import etree as et
from .qb_common_fields_lists_dicts import *
import datetime as dt
from dateutil import parser
from datetime import timedelta, datetime
from .utilities import snake_to_camel

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