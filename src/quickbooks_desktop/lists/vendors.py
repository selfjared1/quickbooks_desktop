from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin
from dataclasses import dataclass

@dataclass
class PrefVendorRef(QBRefMixin):
    class Meta:
        name = "PrefVendorRef"

@dataclass
class TaxVendorRef(QBRefMixin):
    class Meta:
        name = "TaxVendorRef"

@dataclass
class VendorQueryRqType(QBQueryMixin):
    list_id: List[ListId] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[FullName] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
        },
    )
    max_returned: Optional[MaxReturned] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[ActiveStatus] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
        },
    )
    from_modified_date: Optional[FromModifiedDate] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[ToModifiedDate] = field(
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
    total_balance_filter: Optional[TotalBalanceFilter] = field(
        default=None,
        metadata={
            "name": "TotalBalanceFilter",
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
    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
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
    owner_id: List[OwnerId] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    meta_data: VendorQueryRqTypeMetaData = field(
        default=VendorQueryRqTypeMetaData.NO_META_DATA,
        metadata={
            "name": "metaData",
            "type": "Attribute",
        },
    )
    iterator: Optional[VendorQueryRqTypeIterator] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iterator_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "iteratorID",
            "type": "Attribute",
        },
    )