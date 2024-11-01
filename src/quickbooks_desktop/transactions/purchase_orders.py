from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    VendorAddressBlock, ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, VendorAddress, ShipAddress, ShipAddressBlock, LinkedTxn,
)
from src.quickbooks_desktop.lists import (
    VendorRef, ClassInQBRef, InventorySiteRef, ItemRef, InventorySiteLocationRef,
    TermsRef, SalesTaxCodeRef, TemplateRef, ShipMethodRef, CustomerRef, OverrideItemAccountRef,
    ItemGroupRef, OverrideUomsetRef, CurrencyRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin, QBRefMixin, QBMixin
)

@dataclass
class ShipToEntityRef(QBRefMixin):
    class Meta:
        name = "ShipToEntityRef"


@dataclass
class PurchaseOrderLineAdd(QBMixin):
    FIELD_ORDER = [
        "ItemRef", "ManufacturerPartNumber", "Desc", "Quantity", "UnitOfMeasure",
        "Rate", "ClassRef", "Amount", "InventorySiteLocationRef", "CustomerRef",
        "ServiceDate", "OverrideItemAccountRef", "Other1", "Other2", "DataExt"
    ]

    class Meta:
        name = "PurchaseOrderLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
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
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class PurchaseOrderLineGroupAdd(QBMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "PurchaseOrderLineGroupAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLineMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "ManufacturerPartNumber", "Desc", "Quantity",
        "UnitOfMeasure", "OverrideUOMSetRef", "Rate", "ClassRef", "Amount",
        "InventorySiteLocationRef", "CustomerRef", "ServiceDate",
        "IsManuallyClosed", "OverrideItemAccountRef", "Other1", "Other2"
    ]

    class Meta:
        name = "PurchaseOrderLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
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
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )


@dataclass
class PurchaseOrderLineGroupMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "PurchaseOrderLineMod"
    ]

    class Meta:
        name = "PurchaseOrderLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    purchase_order_line_mod: List[PurchaseOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineMod",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "ManufacturerPartNumber", "Desc",
        "Quantity", "UnitOfMeasure", "OverrideUOMSetRef", "Rate",
        "ClassRef", "Amount", "InventorySiteLocationRef", "CustomerRef",
        "ServiceDate", "ReceivedQuantity", "UnbilledQuantity", "IsBilled",
        "IsManuallyClosed", "Other1", "Other2", "DataExtRet"
    ]

    class Meta:
        name = "PurchaseOrderLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
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
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    received_quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "ReceivedQuantity",
            "type": "Element",
        },
    )
    unbilled_quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "UnbilledQuantity",
            "type": "Element",
        },
    )
    is_billed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsBilled",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 29,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "IsPrintItemsInGroup", "TotalAmount",
        "PurchaseOrderLineRet", "DataExtRet"
    ]

    class Meta:
        name = "PurchaseOrderLineGroup"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
            "required": True,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ServiceDate",
            "type": "Element",
        },
    )
    purchase_order_line_ret: List[PurchaseOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineRet",
            "type": "Element",
        },
    )
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeLinkedTxns",
        "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "PurchaseOrderQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
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
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
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
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrderAdd(QBAddMixin):
    FIELD_ORDER = [
        "VendorRef", "ClassRef", "InventorySiteRef", "ShipToEntityRef",
        "TemplateRef", "TxnDate", "RefNumber", "VendorAddress",
        "ShipAddress", "TermsRef", "DueDate", "ExpectedDate",
        "ShipMethodRef", "FOB", "Memo", "VendorMsg", "IsToBePrinted",
        "IsToBeEmailed", "Other1", "Other2", "ExchangeRate",
        "ExternalGUID", "PurchaseOrderLineAdd", "PurchaseOrderLineGroupAdd"
    ]

    class Meta:
        name = "PurchaseOrderAdd"

    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
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
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
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
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    purchase_order_line_add: List[PurchaseOrderLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineAdd",
            "type": "Element",
        },
    )
    purchase_order_line_group_add: List[PurchaseOrderLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class PurchaseOrderMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "VendorRef", "ClassRef", "InventorySiteRef",
        "ShipToEntityRef", "TemplateRef", "TxnDate", "RefNumber", "VendorAddress",
        "ShipAddress", "TermsRef", "DueDate", "ExpectedDate", "ShipMethodRef",
        "FOB", "IsManuallyClosed", "Memo", "VendorMsg", "IsToBePrinted",
        "IsToBeEmailed", "Other1", "Other2", "ExchangeRate",
        "PurchaseOrderLineMod", "PurchaseOrderLineGroupMod"
    ]

    class Meta:
        name = "PurchaseOrderMod"

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
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
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
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
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
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    purchase_order_line_mod: List[PurchaseOrderLineMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineMod",
            "type": "Element",
        },
    )
    purchase_order_line_group_mod: List[PurchaseOrderLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupMod",
            "type": "Element",
        },
    )

@dataclass
class PurchaseOrder(QBMixinWithQuery):

    class Meta:
        name = "PurchaseOrder"

    Query: Type[PurchaseOrderQuery] = PurchaseOrderQuery
    Add: Type[PurchaseOrderAdd] = PurchaseOrderAdd
    Mod: Type[PurchaseOrderMod] = PurchaseOrderMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
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
    txn_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnNumber",
            "type": "Element",
        },
    )
    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
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
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    ship_to_entity_ref: Optional[ShipToEntityRef] = field(
        default=None,
        metadata={
            "name": "ShipToEntityRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    vendor_address_block: Optional[VendorAddressBlock] = field(
        default=None,
        metadata={
            "name": "VendorAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
            "type": "Element",
        },
    )
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    expected_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
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
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    total_amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmountInHomeCurrency",
            "type": "Element",
        },
    )
    is_manually_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsManuallyClosed",
            "type": "Element",
        },
    )
    is_fully_received: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFullyReceived",
            "type": "Element",
        },
    )
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    vendor_msg: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorMsg",
            "type": "Element",
            "max_length": 99,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    other1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other1",
            "type": "Element",
            "max_length": 25,
        },
    )
    other2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other2",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    purchase_order_line_ret: List[PurchaseOrderLine] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineRet",
            "type": "Element",
        },
    )
    purchase_order_line_group_ret: List[PurchaseOrderLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "PurchaseOrderLineGroupRet",
            "type": "Element",
        },
    )
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class PurchaseOrders(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "PurchaseOrder"
        plural_of = PurchaseOrder