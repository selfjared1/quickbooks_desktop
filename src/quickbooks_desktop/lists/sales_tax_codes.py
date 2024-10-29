from dataclasses import dataclass, field
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.common.qb_query_common_fields import NameFilter, NameRangeFilter

@dataclass
class ItemPurchaseTaxRef(QBRefMixin):
    class Meta:
        name = "ItemPurchaseTaxRef"

@dataclass
class PurchaseTaxCodeRef(QBRefMixin):
    class Meta:
        name = "PurchaseTaxCodeRef"


@dataclass
class SalesTaxCodeRef(QBRefMixin):
    class Meta:
        name = "SalesTaxCodeRef"

@dataclass
class ItemSalesTaxRef(QBRefMixin):
    class Meta:
        name = "ItemSalesTaxRef"


@dataclass
class SalesTaxCodeQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "SalesTaxCodeQuery"

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
class SalesTaxCodeAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "IsTaxable", "Desc"
    ]
    
    class Meta:
        name = "SalesTaxCodeAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )


@dataclass
class SalesTaxCodeMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive",
        "IsTaxable", "Desc"
    ]

    class Meta:
        name = "SalesTaxCodeMod"

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
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )



@dataclass
class SalesTaxCode(QBMixinWithQuery):
    class Meta:
        name = "SalesTaxCode"

    Query: Type[SalesTaxCodeQuery] = SalesTaxCodeQuery
    Add: Type[SalesTaxCodeAdd] = SalesTaxCodeAdd
    Mod: Type[SalesTaxCodeMod] = SalesTaxCodeMod

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
            "max_length": 3,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
            "type": "Element",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 31,
        },
    )
    item_purchase_tax_ref: Optional[ItemPurchaseTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemPurchaseTaxRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )

class SalesTaxCodes(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "SalesTaxCode"
        plural_of = SalesTaxCode