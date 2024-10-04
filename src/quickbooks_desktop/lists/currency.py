from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.qb_mixin import QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin
from src.quickbooks_desktop.qb_query_common_fields import NameFilter, NameRangeFilter


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
        },
    )
    thousand_separator_grouping: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThousandSeparatorGrouping",
            "type": "Element",
        },
    )
    decimal_places: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalPlaces",
            "type": "Element",
        },
    )
    decimal_separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "DecimalSeparator",
            "type": "Element",
        },
    )

    VALID_THOUSAND_SEPARATOR_VALUES = ["Comma", "Period", "Space", "Apostrophe"]
    VALID_THOUSAND_SEPARATOR_GROUPING_VALUES = ["Comma", "Period", "Space", "Apostrophe"]
    VALID_DECIMAL_PLACES_VALUES = ["0", "2"]
    VALID_DECIMAL_SEPARATOR_VALUES = ["Period", "Comma"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('thousand_separator', self.thousand_separator, self.VALID_THOUSAND_SEPARATOR_VALUES)
        self._validate_str_from_list_of_values('thousand_separator_grouping', self.thousand_separator_grouping, self.VALID_THOUSAND_SEPARATOR_GROUPING_VALUES)
        self._validate_str_from_list_of_values('decimal_places', self.decimal_places, self.VALID_DECIMAL_PLACES_VALUES)
        self._validate_str_from_list_of_values('decimal_separator', self.decimal_separator, self.VALID_DECIMAL_SEPARATOR_VALUES)


@dataclass
class CurrencyQuery(QBQueryMixin):

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
class Currency(QBMixinWithQuery):
    class Meta:
        name = "Currency"

    class Query(CurrencyQuery):
        pass


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
