from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime, QBDateTime
from src.quickbooks_desktop.common import (
    BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter,
    RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, CreditCardTxnInfo
)
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, ItemSalesTaxRef, TemplateRef, CustomerRef, ClassInQBRef,
    CurrencyRef, SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef,
    ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PriceLevelRef,
    OverrideItemAccountRef, AccountRef,
    PaymentMethodRef, DepositToAccountRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class SalesReceiptLineAdd(QBMixin):
    FIELD_ORDER = [
        "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "Rate", "RatePercent",
        "PriceLevelRef", "ClassRef", "Amount", "OptionForPriceRuleConflict",
        "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "ServiceDate", "SalesTaxCodeRef", "OverrideItemAccountRef",
        "Other1", "Other2", "CreditCardTxnInfo", "DataExt"
    ]

    class Meta:
        name = "SalesReceiptLineAdd"

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
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
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
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class SalesReceiptLineMod(QBModMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "PriceLevelRef", "ClassRef", "Amount",
        "OptionForPriceRuleConflict", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "ServiceDate", "SalesTaxCodeRef",
        "OverrideItemAccountRef", "Other1", "Other2"
    ]

    class Meta:
        name = "SalesReceiptLineMod"

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
class SalesReceiptLineGroupAdd(QBMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "SalesReceiptLineGroupAdd"

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
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLineGroupMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "SalesReceiptLineMod"
    ]

    class Meta:
        name = "SalesReceiptLineGroupMod"

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
    sales_receipt_line_mod: List[SalesReceiptLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineMod",
            "type": "Element",
        },
    )


@dataclass
class SalesReceiptLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "Desc", "Quantity", "UnitOfMeasure", "OverrideUOMSetRef",
        "Rate", "RatePercent", "ClassRef", "Amount", "InventorySiteRef",
        "InventorySiteLocationRef", "SerialNumber", "LotNumber", "ServiceDate",
        "SalesTaxCodeRef", "Other1", "Other2", "CreditCardTxnInfo", "DataExtRet"
    ]

    class Meta:
        name = "SalesReceiptLine"

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
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
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
class SalesReceiptLineGroup(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Desc", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "IsPrintItemsInGroup", "TotalAmount",
        "SalesReceiptLineRet", "DataExtRet"
    ]

    class Meta:
        name = "SalesReceiptLineGroup"

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
    sales_receipt_line_ret: List[SalesReceiptLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineRet",
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
class SalesReceiptQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "SalesReceiptQuery"

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
class SalesReceiptAdd(QBAddMixin):
    FIELD_ORDER = [
        "CustomerRef", "ClassRef", "TemplateRef", "TxnDate", "RefNumber",
        "BillAddress", "ShipAddress", "IsPending", "CheckNumber",
        "PaymentMethodRef", "DueDate", "SalesRepRef", "ShipDate",
        "ShipMethodRef", "FOB", "ItemSalesTaxRef", "Memo", "CustomerMsgRef",
        "IsToBePrinted", "IsToBeEmailed", "CustomerSalesTaxCodeRef",
        "DepositToAccountRef", "CreditCardTxnInfo", "Other", "ExchangeRate",
        "ExternalGUID", "SalesReceiptLineAdd", "SalesReceiptLineGroupAdd"
    ]

    class Meta:
        name = "SalesReceiptAdd"

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
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
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
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
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
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    sales_receipt_line_add: List[SalesReceiptLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineAdd",
            "type": "Element",
        },
    )
    sales_receipt_line_group_add: List[SalesReceiptLineGroupAdd] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupAdd",
            "type": "Element",
        },
    )

@dataclass
class SalesReceiptMod(QBModMixin):
    FIELD_ORDER_SALES_RECEIPT_MOD = [
        "TxnID", "EditSequence", "CustomerRef", "ClassRef", "TemplateRef", "TxnDate",
        "RefNumber", "BillAddress", "ShipAddress", "IsPending", "CheckNumber",
        "PaymentMethodRef", "DueDate", "SalesRepRef", "ShipDate", "ShipMethodRef",
        "FOB", "ItemSalesTaxRef", "Memo", "CustomerMsgRef", "IsToBePrinted",
        "IsToBeEmailed", "CustomerSalesTaxCodeRef", "DepositToAccountRef",
        "Other", "ExchangeRate", "SalesReceiptLineMod", "SalesReceiptLineGroupMod"
    ]
    
    class Meta:
        name = "SalesReceiptMod"

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
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
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
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
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
    sales_receipt_line_mod: List[SalesReceiptLineMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineMod",
            "type": "Element",
        },
    )
    sales_receipt_line_group_mod: List[SalesReceiptLineGroupMod] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupMod",
            "type": "Element",
        },
    )
    
    
@dataclass
class SalesReceipt(QBMixinWithQuery):
    class Meta:
        name = "SalesReceipt"
        
    Query: Type[SalesReceiptQuery] = SalesReceiptQuery
    Add: Type[SalesReceiptAdd] = SalesReceiptAdd
    Mod: Type[SalesReceiptMod] = SalesReceiptMod
        
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
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
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
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
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    credit_card_txn_info: Optional[CreditCardTxnInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInfo",
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
    sales_receipt_line_ret: List[SalesReceiptLine] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineRet",
            "type": "Element",
        },
    )
    sales_receipt_line_group_ret: List[SalesReceiptLineGroup] = field(
        default_factory=list,
        metadata={
            "name": "SalesReceiptLineGroupRet",
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
class SalesReceipts(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "SalesReceipt"
        plural_of = SalesReceipt