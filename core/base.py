from typing import Optional
from core.special_fields import DataExtRet, QBDate
from core.mixins import ToXmlMixin, FromXMLMixin, ToDictMixin, SaveMixin
import attr


@attr.s(auto_attribs=True)
class QBBaseMixin(ToXmlMixin, FromXMLMixin, ToDictMixin, SaveMixin):
    list_dict: dict = {}
    TimeCreated: Optional[QBDate] = attr.ib(default=None, metadata={'is_required': {'Add': None, 'Mod': False, 'Query': None}})
    TimeModified: Optional[QBDate] = attr.ib(default=None, metadata={'is_required': {'Add': None, 'Mod': False, 'Query': None}})
    EditSequence: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': None, 'Mod': True, 'Query': None}})
    DataExtRet: Optional[DataExtRet] = attr.ib(default=None, metadata={'is_required': {'Add': None, 'Mod': False, 'Query': None}})

    def to_ref(self):
        pass

@attr.s(auto_attribs=True)
class QBListBase(QBBaseMixin):
    """
    This is for all list items in QuickBooks Desktop
    """
    ListID: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': None, 'Mod': True, 'Query': False}})

    # todo: def create_list(self):
    # todo: def update_list(self, ignore_none=False):

@attr.s(auto_attribs=True)
class QBContactBase(QBListBase):
    """
    This is for all contact items in QuickBooks Desktop
    """
    CompanyName: Optional[str] = None
    Salutation: Optional[str] = None
    FirstName: Optional[str] = None
    MiddleName: Optional[str] = None
    LastName: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    AccountNumber: Optional[str] = None

@attr.s(auto_attribs=True)
class QBAddressBlock:
    Addr1: Optional[str] = None
    Addr2: Optional[str] = None
    Addr3: Optional[str] = None
    Addr4: Optional[str] = None
    Addr5: Optional[str] = None


@attr.s(auto_attribs=True)
class QBAddress(QBAddressBlock):
    City: Optional[str] = None
    State: Optional[str] = None
    PostalCode: Optional[str] = None
    Country: Optional[str] = None
    Note: Optional[str] = None

@attr.s(auto_attribs=True)
class QBTransactionBase(QBBaseMixin):
    """" Multi currency is not supported yet"""
    class_dict = {
        **QBBaseMixin.class_dict,
        "TxnDate": QBDate,
    }
    TxnID: Optional[str] = None
    TxnDate: Optional[QBDate] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': False}})
    # todo: def create_txn(self):
    # todo: def update_txn(self, ignore_none=False):
