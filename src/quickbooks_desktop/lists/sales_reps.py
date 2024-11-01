from dataclasses import dataclass, field
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime, QBDateTime
from src.quickbooks_desktop.common import NameFilter, NameRangeFilter





@dataclass
class SalesRepQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "SalesRepQuery"

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
class SalesRepAdd(QBAddMixin):
    FIELD_ORDER = [
        "Initial", "IsActive", "SalesRepEntityRef"
    ]

    class Meta:
        name = "SalesRepAdd"

    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "required": True,
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SalesRepMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Initial", "IsActive",
        "SalesRepEntityRef"
    ]

    class Meta:
        name = "SalesRepMod"

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
    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
        },
    )


@dataclass
class SalesRep(QBMixinWithQuery):

    class Meta:
        name = "SalesRep"

    Query: Type[SalesRepQuery] = SalesRepQuery
    Add: Type[SalesRepAdd] = SalesRepAdd
    Mod: Type[SalesRepMod] = SalesRepMod

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
    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "max_length": 5,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
        },
    )

class SalesReps(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "SalesRep"
        plural_of = SalesRep