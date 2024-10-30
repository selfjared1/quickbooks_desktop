from dataclasses import dataclass, field
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin, PluralListSaveMixin
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.common.qb_query_common import NameFilter, NameRangeFilter
from src.quickbooks_desktop.common import ParentRef

@dataclass
class ClassInQBRef(QBRefMixin):
    class Meta:
        name = "ClassRef"


@dataclass
class DiscountClassRef(QBRefMixin):
    class Meta:
        name = "DiscountClassRef"


@dataclass
class ClassInQBQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "ClassQuery"

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
class ClassInQBAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "ClassAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )


@dataclass
class ClassInQBMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentRef"
    ]

    class Meta:
        name = "ClassMod"

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
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
@dataclass
class ClassInQB(QBMixinWithQuery):

    class Meta:
        name = "Class"

    Query: Type[ClassInQBQuery] = ClassInQBQuery
    Add: Type[ClassInQBAdd] = ClassInQBAdd
    Mod: Type[ClassInQBMod] = ClassInQBMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element"
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element"
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31
        },
    )
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element"
        },
    )
    parent_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element"
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element"
        },
    )


class ClassesInQB(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Class"
        plural_of = ClassInQB

