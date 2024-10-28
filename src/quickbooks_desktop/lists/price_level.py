from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBMixin, QBModMixin
)
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import ParentRef, NameFilter, NameRangeFilter, CurrencyFilter
from src.quickbooks_desktop.lists import ItemRef, CurrencyRef



@dataclass
class PriceLevelRef(QBRefMixin):

    class Meta:
        name = "PriceLevelRef"


@dataclass
class PriceLevelPerItem(QBMixin):
    class Meta:
        name = "PriceLevelPerItem"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomPrice",
            "type": "Element",
        },
    )
    custom_price_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "CustomPricePercent",
            "type": "Element",
        },
    )
    adjust_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "AdjustPercentage",
            "type": "Element",
        },
    )
    adjust_relative_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "AdjustRelativeTo",
            "type": "Element",
            "valid_values": ["StandardPrice", "Cost", "CurrentCustomPrice"],
        },
    )


@dataclass
class PriceLevelPerItemRet:
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    custom_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CustomPrice",
            "type": "Element",
        },
    )
    custom_price_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "CustomPricePercent",
            "type": "Element",
        },
    )


@dataclass
class PriceLevelQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ItemRef", "CurrencyFilter",
        "IncludeRetElement"
    ]

    class Meta:
        name = "PriceLevelQuery"

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
    active_status: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
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
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
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
class PriceLevelAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "PriceLevelFixedPercentage",
        "PriceLevelPerItem", "CurrencyRef"
    ]

    class Meta:
        name = "PriceLevelAdd"

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
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item: List[PriceLevelPerItem] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItem",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class PriceLevelMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive",
        "PriceLevelFixedPercentage", "PriceLevelPerItem",
        "CurrencyRef"
    ]

    class Meta:
        name = "PriceLevelMod"

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
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item: List[PriceLevelPerItem] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItem",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class PriceLevel(QBMixinWithQuery):

    class Meta:
        name = "PriceLevel"

    Query: Type[PriceLevelQuery] = PriceLevelQuery
    Add: Type[PriceLevelAdd] = PriceLevelAdd
    Mod: Type[PriceLevelMod] = PriceLevelMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    time_created: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBTime] = field(
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
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    price_level_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PriceLevelType",
            "type": "Element",
            "valid_values": ["FixedPercentage", "PerItem"]
        },
    )
    price_level_fixed_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "PriceLevelFixedPercentage",
            "type": "Element",
        },
    )
    price_level_per_item_ret: List[PriceLevelPerItemRet] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelPerItemRet",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )

class PriceLevels(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "PriceLevel"
        plural_of = PriceLevel
