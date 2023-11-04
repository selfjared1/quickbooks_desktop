from lxml import etree
import attr
from datetime import datetime
from typing import List, Union



@attr.s(auto_attribs=True)
class TimeTrackingQueryRq:
    TxnID: str = None
    TimeCreated: datetime = None
    TimeModified: datetime = None
    EditSequence: str = None
    TxnNumber: int = None
    TxnDate: datetime = None
    defMacro: str = None
    EntityRef_ListID: str = None
    EntityRef_FullName: str = None
    CustomerRef_ListID: str = None
    CustomerRef_FullName: str = None
    ItemServiceRef_ListID: str = None
    ItemServiceRef_FullName: str = None
    Duration: str = None  # Assuming TIMEINTERVALTYPE can be represented as str
    ClassRef_ListID: str = None
    ClassRef_FullName: str = None
    PayrollItemWageRef_ListID: str = None
    PayrollItemWageRef_FullName: str = None
    Notes: str = None
    BillableStatus: str = None
    IsBillable: bool = None
    ExternalGUID: str = None
    IncludeRetElement: List[str] = None
    IsBilled: bool = None
    ErrorRecovery_ListID: str = None
    ErrorRecovery_OwnerID: str = None
    ErrorRecovery_TxnID: str = None
    ErrorRecovery_TxnNumber: int = None
    ErrorRecovery_EditSequence: str = None
    ErrorRecovery_ExternalGUID: str = None
    statusCode: int = None
    statusSeverity: str = None
    statusMessage: str = None

    @classmethod
    def from_xml(cls, xml_string):
        root = etree.fromstring(xml_string)
        params = {
            'metaData': root.get('metaData'),
            'iterator': root.get('iterator'),
            'iteratorID': root.get('iteratorID'),
            'TxnID': [e.text for e in root.findall('./TxnID')],
            'MaxReturned': int(root.findtext('./MaxReturned')) if root.find('./MaxReturned') is not None else None,
            'FromModifiedDate': datetime.strptime(root.findtext('./ModifiedDateRangeFilter/FromModifiedDate'),
                                                  '%Y-%m-%dT%H:%M:%S') if root.find(
                './ModifiedDateRangeFilter/FromModifiedDate') is not None else None,
            'ToModifiedDate': datetime.strptime(root.findtext('./ModifiedDateRangeFilter/ToModifiedDate'),
                                                '%Y-%m-%dT%H:%M:%S') if root.find(
                './ModifiedDateRangeFilter/ToModifiedDate') is not None else None,
            'FromTxnDate': datetime.strptime(root.findtext('./TxnDateRangeFilter/FromTxnDate'),
                                             '%Y-%m-%d') if root.find(
                './TxnDateRangeFilter/FromTxnDate') is not None else None,
            'ToTxnDate': datetime.strptime(root.findtext('./TxnDateRangeFilter/ToTxnDate'), '%Y-%m-%d') if root.find(
                './TxnDateRangeFilter/ToTxnDate') is not None else None,
            'DateMacro': root.findtext('./TxnDateRangeFilter/DateMacro'),
            'ListID': [e.text for e in root.findall('./TimeTrackingEntityFilter/ListID')],
            'FullName': [e.text for e in root.findall('./TimeTrackingEntityFilter/FullName')],
            'IncludeRetElement': [e.text for e in root.findall('./IncludeRetElement')],
        }
        return cls(**params)

    def to_xml(self):
        root = etree.Element("TimeTrackingQueryRq", metaData=self.metaData, iterator=self.iterator,
                             iteratorID=self.iteratorID)

        if self.TxnID is not None:
            for txn_id in self.TxnID:
                etree.SubElement(root, "TxnID").text = txn_id

        if self.MaxReturned is not None:
            etree.SubElement(root, "MaxReturned").text = str(self.MaxReturned)

        if self.FromModifiedDate is not None or self.ToModifiedDate is not None:
            date_filter = etree.SubElement(root, "ModifiedDateRangeFilter")
            if self.FromModifiedDate is not None:
                etree.SubElement(date_filter, "FromModifiedDate").text = self.FromModifiedDate.strftime(
                    '%Y-%m-%dT%H:%M:%S')
            if self.ToModifiedDate is not None:
                etree.SubElement(date_filter, "ToModifiedDate").text = self.ToModifiedDate.strftime('%Y-%m-%dT%H:%M:%S')

        if self.FromTxnDate is not None or self.ToTxnDate is not None:
            date_filter = etree.SubElement(root, "TxnDateRangeFilter")
            if self.FromTxnDate is not None:
                etree.SubElement(date_filter, "FromTxnDate").text = self.FromTxnDate.strftime('%Y-%m-%d')
            if self.ToTxnDate is not None:
                etree.SubElement(date_filter, "ToTxnDate").text = self.ToTxnDate.strftime('%Y-%m-%d')

        if self.DateMacro is not None:
            date_macro_filter = etree.SubElement(root, "TxnDateRangeFilter")
            etree.SubElement(date_macro_filter, "DateMacro").text = self.DateMacro

        if self.ListID is not None:
            entity_filter = etree.SubElement(root, "TimeTrackingEntityFilter")
            for list_id in self.ListID:
                etree.SubElement(entity_filter, "ListID").text = list_id

        if self.FullName is not None:
            entity_filter = root.find("./TimeTrackingEntityFilter") or etree.SubElement(root,
                                                                                        "TimeTrackingEntityFilter")
            for full_name in self.FullName:
                etree.SubElement(entity_filter, "FullName").text = full_name

        if self.IncludeRetElement is not None:
            for include_ret_element in self.IncludeRetElement:
                etree.SubElement(root, "IncludeRetElement").text = include_ret_element

        return etree.tostring(root, pretty_print=True).decode()
