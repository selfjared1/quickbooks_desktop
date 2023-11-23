from typing import Optional
from lxml import etree
import attr
from core.base import QBTransactionBase
from core.special_fields import Ref, QBDate, DataExtRet, QBTimeInterval, BillableStatus
from core.query_mixins import TxnQuery

class TimeTrackingEntityFilter:
    def __init__(self, ListIDs=None, FullNames=None):
        if ListIDs:
            if isinstance(ListIDs, list):
                self.ListIDs = ListIDs
            elif ListIDs:
                self.ListIDs = [ListIDs]
            else:
                pass
        elif FullNames:
            if isinstance(FullNames, list):
                self.FullNames = FullNames
            elif FullNames:
                self.FullNames = [FullNames]
            else:
                pass
        else:
            pass

    def to_xml(self):
        root = etree.Element('TimeTrackingEntityFilter')
        if self.ListIDs:
            for list_id in self.ListIDs:
                list_id_element = etree.Element('ListID')
                list_id_element.text = list_id
                root.append(list_id_element)
        elif self.FullNames:
            for full_name in self.FullNames:
                full_name = etree.Element('FullName')
                full_name.text = full_name
                root.append(full_name)
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')


class TimeTrackingQuery(TxnQuery):
    def __init__(self, query_dict):
        super().__init__(query_dict)
        self.TimeTrackingEntityFilter = TimeTrackingEntityFilter(**query_dict.get('TimeTrackingEntityFilter', {}))

    def to_xml(self):
        root = super().to_xml()
        if self.TimeTrackingEntityFilter:
            root.append(self.TimeTrackingEntityFilter.to_xml())
        else:
            pass
        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
        return xml_str


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

