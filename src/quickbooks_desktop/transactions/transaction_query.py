from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime, QBDateTime
from src.quickbooks_desktop.common import (
    RefNumberFilter, RefNumberRangeFilter,
)
from src.quickbooks_desktop.lists import (
    EntityRef, AccountRef, CurrencyRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, QBMixinWithQuery, QBMixin, QBQueryMixin,
)


@dataclass
class TransactionModifiedDateRangeFilter(QBMixin):
    FIELD_ORDER = [
        "FromModifiedDate", "ToModifiedDate", "DateMacro"
    ]

    class Meta:
        name = "TransactionModifiedDateRangeFilter"

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
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )


@dataclass
class TransactionDateRangeFilter(QBMixin):
    FIELD_ORDER = [
        "FromTxnDate", "ToTxnDate", "DateMacro"
    ]

    class Meta:
        name = "TransactionDateRangeFilter"

    from_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromTxnDate",
            "type": "Element",
        },
    )
    to_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToTxnDate",
            "type": "Element",
        },
    )
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )


@dataclass
class TransactionEntityFilter(QBMixin):
    FIELD_ORDER = [
        "EntityTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionEntityFilter"

    entity_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "EntityTypeFilter",
            "type": "Element",
            "valid_values": ["Customer", "Employee", "OtherName", "Vendor"]
        },
    )
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
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
            "max_length": 36,
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionAccountFilter(QBMixin):
    FIELD_ORDER = [
        "AccountTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionAccountFilter"

    account_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountTypeFilter",
            "type": "Element",
            "valid_values": [
                "AccountsPayable", "AccountsReceivable", "AllowedFor1099", "APAndSalesTax",
                "APOrCreditCard", "ARAndAP", "Asset", "BalanceSheet", "Bank",
                "BankAndARAndAPAndUF", "BankAndUF", "CostOfSales", "CreditCard",
                "CurrentAsset", "CurrentAssetAndExpense", "CurrentLiability", "Equity",
                "EquityAndIncomeAndExpense", "ExpenseAndOtherExpense", "FixedAsset",
                "IncomeAndExpense", "IncomeAndOtherIncome", "Liability", "LiabilityAndEquity",
                "LongTermLiability", "NonPosting", "OrdinaryExpense", "OrdinaryIncome",
                "OrdinaryIncomeAndCOGS", "OrdinaryIncomeAndExpense", "OtherAsset",
                "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense",
                "OtherIncome", "OtherIncomeOrExpense"
            ],
        },
    )
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
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
            "max_length": 36,
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionItemFilter(QBMixin):
    FIELD_ORDER = [
        "ItemTypeFilter", "ListID", "FullName",
        "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionItemFilter"

    item_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemTypeFilter",
            "type": "Element",
            "valid_values": [
                "AllExceptFixedAsset", "Assembly", "Discount", "FixedAsset", "Inventory",
                "InventoryAndAssembly", "NonInventory", "OtherCharge", "Payment",
                "Sales", "SalesTax", "Service"
            ]
        },
    )
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
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class TransactionClassFilter(QBMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "ListIDWithChildren", "FullNameWithChildren"
    ]

    class Meta:
        name = "TransactionClassFilter"

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
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )


@dataclass
class CurrencyFilter(QBMixin):
    FIELD_ORDER = [
        "ListID", "FullName"
    ]

    class Meta:
        name = "CurrencyFilter"

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
            "max_length": 64,
        },
    )


@dataclass
class TransactionQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "RefNumber", "RefNumberCaseSensitive",
        "RefNumberFilter", "RefNumberRangeFilter", "TransactionModifiedDateRangeFilter",
        "TransactionDateRangeFilter", "TransactionEntityFilter",
        "TransactionAccountFilter", "TransactionItemFilter", "TransactionClassFilter",
        "TransactionTypeFilter", "TransactionDetailLevelFilter",
        "TransactionPostingStatusFilter", "TransactionPaidStatusFilter",
        "CurrencyFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "TransactionQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
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
    transaction_modified_date_range_filter: Optional[
        TransactionModifiedDateRangeFilter
    ] = field(
        default=None,
        metadata={
            "name": "TransactionModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    transaction_date_range_filter: Optional[TransactionDateRangeFilter] = (
        field(
            default=None,
            metadata={
                "name": "TransactionDateRangeFilter",
                "type": "Element",
            },
        )
    )
    transaction_entity_filter: Optional[TransactionEntityFilter] = field(
        default=None,
        metadata={
            "name": "TransactionEntityFilter",
            "type": "Element",
        },
    )
    transaction_account_filter: Optional[TransactionAccountFilter] = field(
        default=None,
        metadata={
            "name": "TransactionAccountFilter",
            "type": "Element",
        },
    )
    transaction_item_filter: Optional[TransactionItemFilter] = field(
        default=None,
        metadata={
            "name": "TransactionItemFilter",
            "type": "Element",
        },
    )
    transaction_class_filter: Optional[TransactionClassFilter] = field(
        default=None,
        metadata={
            "name": "TransactionClassFilter",
            "type": "Element",
        },
    )
    transaction_type_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionTypeFilter",
            "type": "Element",
            "valid_values": [
                "All", "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
                "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit",
                "YTDAdjustment"
            ],
        },
    )
    transaction_detail_level_filter: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "TransactionDetailLevelFilter",
                "type": "Element",
                "valid_values": [
                    "All", "SummaryOnly", "AllExceptSummary"
                ],
            },
        )
    )
    transaction_posting_status_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionPostingStatusFilter",
            "type": "Element",
            "valid_values": [
                "All", "SummaryOnly", "AllExceptSummary"
            ],
        },
    )
    transaction_paid_status_filter: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "TransactionPaidStatusFilter",
                "type": "Element",
                "valid_values": [
                    "Either", "Closed", "Open"
                ],
            },
        )
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
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


@dataclass
class Transaction(QBMixinWithQuery):

    class Meta:
        name = "Transaction"

    Query: Type[TransactionQuery] = TransactionQuery
    #No Add
    #No Mod

    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
                "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit",
                "YTDAdjustment"
            ],
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
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
    entity_ref: Optional[EntityRef] = field(
        default=None,
        metadata={
            "name": "EntityRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class Transactions(PluralMixin):

    class Meta:
        name = "Transaction"
        plural_of = Transaction