from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List
from src.quickbooks_desktop.data_ext import DataExt

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ExpenseLineMod,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, VendorAddress,
    ItemLineAdd, ExpenseLineAdd, ItemGroupLineAdd, ItemLineMod, ItemGroupLineMod, LinkedTxn, ExpenseLine,
    ItemLine, ItemGroupLine
)
from src.quickbooks_desktop.lists import (
    CurrencyRef, VendorRef,
    ApaccountRef, TermsRef, SalesTaxCodeRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)

@dataclass
class BillQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "PaidStatus", "IncludeLineItems",
        "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BillQuery"

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
            "valid_values": ["All", "PaidOnly", "NotPaidOnly"],
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
class BillAdd(QBAddMixin):
    FIELD_ORDER = [
        "VendorRef", "VendorAddress", "APAccountRef", "TxnDate",
        "DueDate", "RefNumber", "TermsRef", "Memo", "ExchangeRate",
        "ExternalGUID", "LinkToTxnID", "ExpenseLineAdd", "ItemLineAdd",
        "ItemGroupLineAdd"
    ]

    class Meta:
        name = "BillAdd"

    vendor_ref: Optional[VendorRef] = field(
        default=None,
        metadata={
            "name": "VendorRef",
            "type": "Element",
            "required": True,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
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
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
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
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    link_to_txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LinkToTxnID",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
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
class BillMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "VendorRef", "VendorAddress",
        "APAccountRef", "TxnDate", "DueDate", "RefNumber",
        "TermsRef", "Memo", "ExchangeRate", "ClearExpenseLines",
        "ExpenseLineMod", "ClearItemLines", "ItemLineMod",
        "ItemGroupLineMod"
    ]

    class Meta:
        name = "BillMod"

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
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
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
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
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
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )


@dataclass
class Bill(QBMixinWithQuery):

    class Meta:
        name = "Bill"

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
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    apaccount_ref: Optional[ApaccountRef] = field(
        default=None,
        metadata={
            "name": "APAccountRef",
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
    due_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DueDate",
            "type": "Element",
        },
    )
    amount_due: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountDue",
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
    amount_due_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountDueInHomeCurrency",
            "type": "Element",
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "max_length": 20,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
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
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    is_paid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPaid",
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
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    expense_line: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_line_ret: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_line_ret: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
            "type": "Element",
        },
    )
    open_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenAmount",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


class Bills(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Bill"
        plural_of = Bill