from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin, PluralListSaveMixin
from src.quickbooks_desktop.common.qb_query_common_fields import NameFilter, NameRangeFilter


@dataclass
class CurrencyRef(QBRefMixin):
    class Meta:
        name = "CurrencyRef"


@dataclass
class CurrencyFormat(QBMixin):
    thousand_separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThousandSeparator",
            "type": "Element",
            "valid_values": ["Comma", "Period", "Space", "Apostrophe"]
        },
    )
    thousand_separator_grouping: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThousandSeparatorGrouping",
            "type": "Element",
            "valid_values": ["Comma", "Period", "Space", "Apostrophe"]
        },
    )
    decimal_places: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalPlaces",
            "type": "Element",
            "valid_values": ["0", "2"]
        },
    )
    decimal_separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalSeparator",
            "type": "Element",
            "valid_values": ["Period", "Comma"]
        },
    )


@dataclass
class CurrencyQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "CurrencyQuery"

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
    # meta_data: CurrencyQueryRqTypeMetaData = field(
    #     default=CurrencyQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )


@dataclass
class CurrencyAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "CurrencyCode", "CurrencyFormat", "IncludeRetElement"
    ]

    class Meta:
        name = "CurrencyAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "required": True,
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )


@dataclass
class CurrencyMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "CurrencyCode",
        "CurrencyFormat"
    ]

    class Meta:
        name = "CurrencyMod"

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
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )


@dataclass
class Currency(QBMixinWithQuery):
    class Meta:
        name = "Currency"

    Query: Type[CurrencyQuery] = CurrencyQuery
    Add: Type[CurrencyAdd] = CurrencyAdd
    Mod: Type[CurrencyMod] = CurrencyMod

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
            "max_length": 64,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "max_length": 3,
        },
    )
    currency_format: Optional[CurrencyFormat] = field(
        default=None,
        metadata={
            "name": "CurrencyFormat",
            "type": "Element",
        },
    )
    is_user_defined_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsUserDefinedCurrency",
            "type": "Element",
        },
    )
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    as_of_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AsOfDate",
            "type": "Element",
        },
    )


class Currencies(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Currency"
        plural_of = Currency
