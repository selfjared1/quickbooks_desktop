import dateutil.parser as parser
import datetime as dt


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

class DataExtRet:
    def __init__(self,
                 OwnerID: str = None,
                 DataExtName: str = None,
                 DataExtType: str = None,
                 DataExtValue: str = None,
                 ):
        self.OwnerId = OwnerID
        self.DataExtName = DataExtName
        self.DataExtType = DataExtType
        self.DataExtValue = DataExtValue

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

class QBDates:
    def __init__(self, date=None):
        self.check_date_not_none(date)
        self.macro_dict = QBDates.get_macro_dict(self)
        self.date_is_macro = False
        self.date = self.parse_date(date)

    def check_date_not_none(self, date):
        if date == None:
            raise Exception('You did not include a date')

    def parse_date(self, date):
        if isinstance(date, str):
            if date.lower() in self.macro_dict.keys():
                self.__setattr__('date_is_macro', True)
                return self.macro_dict[date.lower()]
            else:
                try:
                    date_parsed = parser.parse(date)
                    date_str = dt.date.strftime("%m/%d/%Y")
                    return date_str
                except Exception as e:
                    raise Exception(f'Your date parameter "{date}" could not be parsed')
        elif isinstance(date, dt.datetime):
            # todo:
            return None
        elif isinstance(date, dt.date):
            # todo:
            return None

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