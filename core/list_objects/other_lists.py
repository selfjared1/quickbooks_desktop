from datetime import datetime
from typing import List
from attrs import define
from utility.utilities import from_lxml_elements
import pandas as pd

@define
class BarCode:
    ListType: str = None  # todo: validate
    ListID: str = None
    FullName: str = None

    @classmethod
    def from_xml(cls, elements):
        account = from_lxml_elements(cls, elements, combine_with_child_list=['TaxLineInfoRet', 'CurrencyRef'])
        return account