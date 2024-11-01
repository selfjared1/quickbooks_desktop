from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type, Dict
from collections import defaultdict
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    LinkedTxn, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, SetCredit,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, LinkToTxn
)
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, ItemSalesTaxRef, TemplateRef, CustomerRef, ClassInQBRef, AraccountRef, CurrencyRef, TermsRef,
    SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef, ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PriceLevelRef, OverrideItemAccountRef, AccountRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class InvoiceLineAdd(QBAddMixin):

    FIELD_ORDER = [
        "item_ref", "desc", "quantity", "unit_of_measure", "rate", "rate_percent",
        "price_level_ref", "class_ref", "amount", "option_for_price_rule_conflict",
        "inventory_site_ref", "inventory_site_location_ref", "serial_number",
        "lot_number", "service_date", "sales_tax_code_ref", "override_item_account_ref",
        "other1", "other2", "link_to_txn", "data_ext"
    ]

    class Meta:
        name = "InvoiceLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
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
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
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
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
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
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
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
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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
    link_to_txn: Optional[LinkToTxn] = field(
        default=None,
        metadata={
            "name": "LinkToTxn",
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
class InvoiceLineMod(QBMixin):

    class Meta:
        name = "InvoiceLineMod"

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
    rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
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
    option_for_price_rule_conflict: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "OptionForPriceRuleConflict",
                "type": "Element",
                "valid_values": ["Zero", "BasePrice"]
            },
        )
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
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
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
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


@dataclass
class InvoiceLine(QBMixin):

    class Meta:
        name = "InvoiceLine"

    Add: Type[InvoiceLineAdd] = InvoiceLineAdd
    # Mod: Type[InvoiceLineMod] = InvoiceLineMod

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
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
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
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
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
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
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
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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
class InvoiceLineGroupAdd(QBAddMixin):

    FIELD_ORDER = [
        "item_group_ref", "quantity", "unit_of_measure", "inventory_site_ref",
        "inventory_site_location_ref", "data_ext"
    ]

    class Meta:
        name = "InvoiceLineGroupAdd"

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
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
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
    # data_ext: List[DataExt] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExt",
    #         "type": "Element",
    #     },
    # )


@dataclass
class InvoiceLineGroupMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "InvoiceLineMod"
    ]

    class Meta:
        name = "InvoiceLineGroupMod"

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
    invoice_line_mod: List[InvoiceLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineMod",
            "type": "Element",
        },
    )


@dataclass
class InvoiceLineGroup(QBMixin):

    class Meta:
        name = "InvoiceLineGroup"

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
    invoice_line_ret: List[InvoiceLine] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineRet",
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
class InvoiceQuery(QBQueryMixin):

    FIELD_ORDER = [
        "txn_id", "ref_number", "ref_number_case_sensitive", "max_returned",
        "modified_date_range_filter", "txn_date_range_filter", "entity_filter",
        "account_filter", "ref_number_filter", "ref_number_range_filter",
        "currency_filter", "paid_status", "include_line_items", "include_linked_txns",
        "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "InvoiceQuery"

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
    paid_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaidStatus",
            "type": "Element",
            "valid_values": ["All", "PaidOnly", "NotPaidOnly"]
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
class InvoiceAdd(QBAddMixin):

    FIELD_ORDER = [
        "customer_ref", "class_ref", "ar_account_ref", "template_ref", "txn_date",
        "ref_number", "bill_address", "ship_address", "is_pending", "is_finance_charge",
        "po_number", "terms_ref", "due_date", "sales_rep_ref", "fob", "ship_date",
        "ship_method_ref", "item_sales_tax_ref", "memo", "customer_msg_ref",
        "is_to_be_printed", "is_to_be_emailed", "customer_sales_tax_code_ref",
        "other", "exchange_rate", "external_guid", "link_to_txn_id", "set_credit",
        "invoice_line_add", "invoice_line_group_add", "include_ret_element"
    ]

    class Meta:
        name = "InvoiceAdd"

    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
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
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    is_finance_charge: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFinanceCharge",
            "type": "Element",
        },
    )
    po_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
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
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
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
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
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
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
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
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    exchange_rate: Optional[Decimal] = field(
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
    link_to_txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LinkToTxnID",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    invoice_line_add: List[InvoiceLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineAdd",
            "type": "Element",
        },
    )
    invoice_line_group_add: List[InvoiceLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupAdd",
            "type": "Element",
        },
    )

    def validate(self):
        super().validate()
        self.is_to_be_emailed = False
        self.is_pending = False
        self.is_to_be_printed = False


@dataclass
class InvoiceMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "ARAccountRef",
        "TemplateRef", "TxnDate", "RefNumber", "BillAddress", "ShipAddress",
        "IsPending", "PONumber", "TermsRef", "DueDate", "SalesRepRef",
        "FOB", "ShipDate", "ShipMethodRef", "ItemSalesTaxRef", "Memo",
        "CustomerMsgRef", "IsToBePrinted", "IsToBeEmailed",
        "CustomerSalesTaxCodeRef", "Other", "ExchangeRate", "SetCredit",
        "InvoiceLineMod", "InvoiceLineGroupMod"
    ]

    class Meta:
        name = "InvoiceMod"

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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
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
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
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
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
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
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
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
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
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
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
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
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    invoice_line_mod: List[InvoiceLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineMod",
            "type": "Element",
        },
    )
    invoice_line_group_mod: List[InvoiceLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupMod",
            "type": "Element",
        },
    )


@dataclass
class Invoice(QBMixinWithQuery):

    class Meta:
        name = "Invoice"

    Query: Type[InvoiceQuery] = InvoiceQuery
    Add: Type[InvoiceAdd] = InvoiceAdd
    Mod: Type[InvoiceMod] = InvoiceMod

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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    ar_account_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
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
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    is_finance_charge: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFinanceCharge",
            "type": "Element",
        },
    )
    po_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
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
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
    ship_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ShipDate",
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
    subtotal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
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
    sales_tax_percentage: Optional[float] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    applied_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
        },
    )
    balance_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
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
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    balance_remaining_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemainingInHomeCurrency",
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
    is_paid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPaid",
            "type": "Element",
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
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
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    suggested_discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountAmount",
            "type": "Element",
        },
    )
    suggested_discount_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountDate",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
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
    invoice_line_ret: List[InvoiceLine] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineRet",
            "type": "Element",
        },
    )
    invoice_line_groups: List[InvoiceLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupRet",
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
class Invoices(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Invoice"
        plural_of = Invoice

    def split_invoices_by_tax(self) -> Dict[str, List[Invoice]]:
        result = defaultdict(list)

        # Group invoices by item_sales_tax_ref and sales_tax_percentage
        for invoice in self:  # Assuming self.invoices holds the list of Invoice objects
            key = f"{invoice.item_sales_tax_ref}-{invoice.sales_tax_percentage}"
            result[key].append(invoice)

        return dict(result)

