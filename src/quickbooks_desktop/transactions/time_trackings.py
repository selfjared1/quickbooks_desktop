from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime, QBDateTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter,
)
from src.quickbooks_desktop.lists import (
    CustomerRef, ClassInQBRef, EntityRef, ItemServiceRef, PayrollItemWageRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class TimeTrackingEntityFilter(QBMixin):
    FIELD_ORDER = [
        "ListId", "FullName",
        ]

    class Meta:
        name = "TimeTrackingEntityFilter"

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


@dataclass
class TimeTrackingQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "TimeTrackingEntityFilter",
        "IncludeRetElement"
    ]

    class Meta:
        name = "TimeTrackingQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
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
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    time_tracking_entity_filter: Optional[TimeTrackingEntityFilter] = field(
        default=None,
        metadata={
            "name": "TimeTrackingEntityFilter",
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
class TimeTrackingAdd(QBAddMixin):
    FIELD_ORDER = [
        "TxnDate", "EntityRef", "CustomerRef", "ItemServiceRef",
        "Duration", "ClassRef", "PayrollItemWageRef", "Notes",
        "BillableStatus", "IsBillable", "ExternalGUID"
    ]

    class Meta:
        name = "TimeTrackingAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
            "required": True,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
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
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
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
class TimeTrackingMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "EntityRef",
        "CustomerRef", "ItemServiceRef", "Duration", "ClassRef",
        "PayrollItemWageRef", "Notes", "BillableStatus"
    ]

    class Meta:
        name = "TimeTrackingMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
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
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
            "type": "Element",
            "required": True,
        },
    )
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "required": True,
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
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
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )


@dataclass
class TimeTracking(QBMixinWithQuery):
    
    class Meta:
        name = "TimeTracking"

    Query: Type[TimeTrackingQuery] = TimeTrackingQuery
    Add: Type[TimeTrackingAdd] = TimeTrackingAdd
    Mod: Type[TimeTrackingMod] = TimeTrackingMod
        
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
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
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
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
    item_service_ref: Optional[ItemServiceRef] = field(
        default=None,
        metadata={
            "name": "ItemServiceRef",
            "type": "Element",
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    duration: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "Duration",
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
    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
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
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
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
class TimeTrackings(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "TimeTracking"
        plural_of = TimeTracking