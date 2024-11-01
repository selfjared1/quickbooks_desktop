from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter,
    RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter,
)
from src.quickbooks_desktop.lists import (
    ItemSalesTaxRef, ClassInQBRef, CurrencyRef, AccountRef,
    EntityRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class JournalDebitLine(QBMixin):
    FIELD_ORDER = ["TxnLineID", "AccountRef", "Amount", "Memo", "EntityRef",
                   "ClassRef", "BillableStatus"]

    class Meta:
        name = "JournalDebitLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
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
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
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
class JournalCreditLine(QBMixin):
    FIELD_ORDER = ["TxnLineID", "AccountRef", "Amount", "Memo", "EntityRef",
                   "ClassRef", "BillableStatus"]

    class Meta:
        name = "JournalCreditLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
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
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
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
class JournalLineMod(QBMixin):
    class Meta:
        name = "JournalLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    journal_line_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "JournalLineType",
            "type": "Element",
            "valid_values": {
                "JournalLineType": ["Debit", "Credit"],
            }

        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
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
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )


@dataclass
class JournalEntryQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "EntityFilter", "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "JournalEntryQuery"

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
class JournalEntryAdd(QBAddMixin):
    FIELD_ORDER = [
        "TxnDate", "RefNumber", "IsAdjustment", "IsHomeCurrencyAdjustment",
        "IsAmountsEnteredInHomeCurrency", "CurrencyRef", "ExchangeRate",
        "ExternalGUID", "JournalDebitLine", "JournalCreditLine"
    ]
    
    class Meta:
        name = "JournalEntryAdd"

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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
        },
    )
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    is_home_currency_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsHomeCurrencyAdjustment",
            "type": "Element",
        },
    )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
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
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    journal_debit_line: List[JournalDebitLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalDebitLine",
            "type": "Element",
        },
    )
    journal_credit_line: List[JournalCreditLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalCreditLine",
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
class JournalEntryMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "RefNumber", "IsAdjustment",
        "IsAmountsEnteredInHomeCurrency", "CurrencyRef", "ExchangeRate",
        "JournalLineMod"
    ]

    class Meta:
        name = "JournalEntryMod"

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
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
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
    journal_line_mod: List[JournalLineMod] = field(
        default_factory=list,
        metadata={
            "name": "JournalLineMod",
            "type": "Element",
        },
    )

    
@dataclass
class JournalEntry(QBMixinWithQuery):
    
    class Meta:
        name = "JournalEntry"
        
    Query: Type[JournalEntryQuery] = JournalEntryQuery
    Add: Type[JournalEntryAdd] = JournalEntryAdd
    Mod: Type[JournalEntryMod] = JournalEntryMod
        
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
        },
    )
    is_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAdjustment",
            "type": "Element",
        },
    )
    is_home_currency_adjustment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsHomeCurrencyAdjustment",
            "type": "Element",
        },
    )
    is_amounts_entered_in_home_currency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAmountsEnteredInHomeCurrency",
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
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    journal_debit_line: List[JournalDebitLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalDebitLine",
            "type": "Element",
        },
    )
    journal_credit_line: List[JournalCreditLine] = field(
        default_factory=list,
        metadata={
            "name": "JournalCreditLine",
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
class JournalEntries(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "JournalEntry"
        plural_of = JournalEntry