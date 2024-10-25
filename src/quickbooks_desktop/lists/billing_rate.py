from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.common import NameFilter, NameRangeFilter
from src.quickbooks_desktop.lists import ItemRef
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin, PluralListSaveMixin


FIELD_ORDER = [
    "ListID", "FullName", "MaxReturned", "FromModifiedDate", "ToModifiedDate",
    "NameFilter", "NameRangeFilter", "ItemRef", "IncludeRetElement"
]

@dataclass
class BillingRateRef(QBRefMixin):

    class Meta:
        name = "BillingRateRef"

@dataclass
class BillingRatePerItem(QBMixin):
    FIELD_ORDER = [
        "ItemRef", "CustomRate", "CustomRatePercent", "AdjustPercentage",
        "AdjustBillingRateRelativeTo"
    ]

    class Meta:
        name = "BillingRatePerItem"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomRate",
            "type": "Element",
        },
    )
    custom_rate_percent: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomRatePercent",
            "type": "Element",
        },
    )
    adjust_percentage: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AdjustPercentage",
            "type": "Element",
        },
    )
    adjust_billing_rate_relative_to: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "AdjustBillingRateRelativeTo",
                "type": "Element",
                "valid_value": ["StandardRate", "CurrentCustomRate"]
            },
        )
    )

@dataclass
class BillingRateQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "FromModifiedDate", "ToModifiedDate",
        "NameFilter", "NameRangeFilter", "ItemRef", "IncludeRetElement"
    ]

    class Meta:
        name = "BillingRateQuery"

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
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
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
class BillingRateAdd:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    fixed_billing_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FixedBillingRate",
            "type": "Element",
        },
    )
    billing_rate_per_item: List[BillingRatePerItem] = field(
        default_factory=list,
        metadata={
            "name": "BillingRatePerItem",
            "type": "Element",
        },
    )


@dataclass
class BillingRate(QBMixin):
    class Meta:
        name = "BillingRate"

    Query: Type[BillingRateQuery] = BillingRateQuery
    Add: Type[BillingRateAdd] = BillingRateAdd
    # there is no Mod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    billing_rate_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillingRateType",
            "type": "Element",
            "valid_values": ["FixedRate", "PerItem"]
        },
    )
    fixed_billing_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FixedBillingRate",
            "type": "Element",
        },
    )
    billing_rate_per_item_ret: List[BillingRatePerItem] = field(
        default_factory=list,
        metadata={
            "name": "BillingRatePerItemRet",
            "type": "Element",
        },
    )

class BillingRates(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "BillingRate"
        plural_of = BillingRate


