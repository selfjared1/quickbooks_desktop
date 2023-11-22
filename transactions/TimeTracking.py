from typing import Optional
from lxml import etree
import attr
from core.base import QBTransactionBase
from core.special_fields import Ref, QBDate, DataExtRet, QBTimeInterval, BillableStatus


@attr.s(auto_attribs=True)
class TimeTracking(QBTransactionBase):
    class_dict = {
        **QBTransactionBase.class_dict,
        "EntityRef": Ref,
        "CustomerRef": Ref,
        "ItemServiceRef": Ref,
        "Duration": QBTimeInterval,
        "ClassRef": Ref,
        "PayrollItemWageRef": Ref,
        "DataExtRet": DataExtRet
    }

    TxnNumber: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    EntityRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': True, 'Mod': True, 'Query': None}})
    CustomerRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    ItemServiceRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    Duration: Optional[QBTimeInterval] = attr.ib(default=None, metadata={'is_required': {'Add': True, 'Mod': True, 'Query': None}})  # Assuming TIMEINTERVALTYPE can be represented as str
    ClassRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    PayrollItemWageRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    Notes: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    BillableStatus: Optional[BillableStatus] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    IsBillable: Optional[bool] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    ExternalGUID: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})

