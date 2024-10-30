from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ExpenseLineMod,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, VendorAddress, Address, AddressBlock,
    ItemLineAdd, ExpenseLineAdd, ItemGroupLineAdd, ItemLineMod, ItemGroupLineMod, LinkedTxn, ExpenseLine,
    ItemLine, ItemGroupLine, PayeeEntityRef, AppliedToTxnAdd, AppliedToTxnMod, AppliedToTxn
)
from src.quickbooks_desktop.lists import (
    CurrencyRef, VendorRef, BankAccountRef,
    ApaccountRef, TermsRef, SalesTaxCodeRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)

@dataclass
class BillPaymentCheckQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BillPaymentCheckQuery"

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
class BillPaymentCheckAdd(QBAddMixin):
    FIELD_ORDER = [
        "PayeeEntityRef", "APAccountRef", "TxnDate", "BankAccountRef",
        "IsToBePrinted", "RefNumber", "Memo", "ExchangeRate",
        "ExternalGUID", "AppliedToTxnAdd"
    ]

    class Meta:
        name = "BillPaymentCheckAdd"

    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
            "type": "Element",
            "required": True,
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
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
            "type": "Element",
            "required": True,
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
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
            "max_length": 4095,
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
    applied_to_txn_add: List[AppliedToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnAdd",
            "type": "Element",
            "min_occurs": 1,
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
class BillPaymentCheckMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "BankAccountRef",
        "Amount", "ExchangeRate", "IsToBePrinted", "RefNumber",
        "Memo", "AppliedToTxnMod"
    ]

    class Meta:
        name = "BillPaymentCheckMod"

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
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
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
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
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
            "max_length": 4095,
        },
    )
    applied_to_txn_mod: List[AppliedToTxnMod] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnMod",
            "type": "Element",
        },
    )


@dataclass
class BillPaymentCheck(QBMixinWithQuery):
    
    class Meta:
        name = "BillPaymentCheck"

    Query: Type[BillPaymentCheckQuery] = BillPaymentCheckQuery
    Add: Type[BillPaymentCheckAdd] = BillPaymentCheckAdd
    Mod: Type[BillPaymentCheckMod] = BillPaymentCheckMod
    
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
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
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
    bank_account_ref: Optional[BankAccountRef] = field(
        default=None,
        metadata={
            "name": "BankAccountRef",
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
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
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
            "max_length": 4095,
        },
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    address_block: Optional[AddressBlock] = field(
        default=None,
        metadata={
            "name": "AddressBlock",
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
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_ret: List[AppliedToTxn] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnRet",
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

class BillPaymentChecks(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "BillPaymentCheck"
        plural_of = BillPaymentCheck