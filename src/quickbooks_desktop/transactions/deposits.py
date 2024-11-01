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
    DepositToAccountRef, OverrideClassRef, EntityRef, CustomerRef, ClassInQBRef, AraccountRef, CurrencyRef, TermsRef,
    SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef, ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PaymentMethodRef, OverrideItemAccountRef, AccountRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBRefMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin, SaveMixin
)

VALID_TXN_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
    "BuildAssembly", "Charge", "Check", "Deposit", "CreditCardCredit",
    "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
    "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
    "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
    "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit",
    "YTDAdjustment"
]


@dataclass
class CashBackInfoAdd(QBMixin):
    FIELD_ORDER = [
        "AccountRef", "Memo", "Amount"
    ]

    class Meta:
        name = "CashBackInfoAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )


@dataclass
class CashBackInfoMod(QBModMixin):
    FIELD_ORDER = [
        "AccountRef", "Memo", "Amount"
    ]

    class Meta:
        name = "CashBackInfoMod"
        
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    
@dataclass
class CashBackInfo(QBMixin):
    FIELD_ORDER = [
        "txn_line_id", "AccountRef", "Memo", "Amount"
    ]
    
    class Meta:
        name = "CashBackInfo"
    
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )

@dataclass
class DepositLineAdd(QBMixin):
    FIELD_ORDER = [
        "PaymentTxnID", "PaymentTxnLineID", "OverrideMemo", "OverrideCheckNumber",
        "OverrideClassRef", "EntityRef", "AccountRef", "Memo", "CheckNumber",
        "PaymentMethodRef", "ClassRef", "Amount"
    ]

    class Meta:
        name = "DepositLineAdd"

    payment_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnID",
            "type": "Element",
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
            "type": "Element",
        },
    )
    override_memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideMemo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    override_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideCheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    override_class_ref: Optional[OverrideClassRef] = field(
        default=None,
        metadata={
            "name": "OverrideClassRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class DepositLineMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "PaymentTxnID", "PaymentTxnLineID", "OverrideMemo",
        "OverrideCheckNumber", "OverrideClassRef", "EntityRef", "AccountRef",
        "Memo", "CheckNumber", "PaymentMethodRef", "ClassRef", "Amount"
    ]

    class Meta:
        name = "DepositLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    payment_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnID",
            "type": "Element",
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
            "type": "Element",
        },
    )
    override_memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideMemo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    override_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverrideCheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    override_class_ref: Optional[OverrideClassRef] = field(
        default=None,
        metadata={
            "name": "OverrideClassRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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

@dataclass
class DepositLine(QBMixin):

    class Meta:
        name = "DepositLine"

    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "valid_values": VALID_TXN_TYPE_VALUES
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
            "required": True,
        },
    )
    payment_txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTxnLineID",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckNumber",
            "type": "Element",
            "max_length": 11,
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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


@dataclass
class DepositQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "CurrencyFilter", "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "DepositQuery"

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
class DepositAdd(QBAddMixin):
    FIELD_ORDER = [
        "TxnDate", "DepositToAccountRef", "Memo", "CashBackInfoAdd", "CurrencyRef",
        "ExchangeRate", "ExternalGUID", "DepositLineAdd"
    ]

    class Meta:
        name = "DepositAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
            "required": True,
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
    cash_back_info_add: Optional[CashBackInfoAdd] = field(
        default=None,
        metadata={
            "name": "CashBackInfoAdd",
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
    deposit_line_add: List[DepositLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineAdd",
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
class DepositMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "DepositToAccountRef", "Memo",
        "CashBackInfoMod", "CurrencyRef", "ExchangeRate", "DepositLineMod"
    ]

    class Meta:
        name = "DepositMod"

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
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
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
    cash_back_info_mod: Optional[CashBackInfoMod] = field(
        default=None,
        metadata={
            "name": "CashBackInfoMod",
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
    deposit_line_mod: List[DepositLineMod] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineMod",
            "type": "Element",
        },
    )

    
@dataclass
class Deposit(QBMixinWithQuery):
    
    class Meta:
        name = "NameFilter"

    Query: Type[DepositQuery] = DepositQuery
    Add: Type[DepositAdd] = DepositAdd
    Mod: Type[DepositMod] = DepositMod
    
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
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
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
    deposit_total: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DepositTotal",
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
    deposit_total_in_home_currency: Optional[Decimal] = (
        field(
            default=None,
            metadata={
                "name": "DepositTotalInHomeCurrency",
                "type": "Element",
            },
        )
    )
    cash_back_info_ret: Optional[CashBackInfo] = field(
        default=None,
        metadata={
            "name": "CashBackInfoRet",
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
    deposit_line_ret: List[DepositLine] = field(
        default_factory=list,
        metadata={
            "name": "DepositLineRet",
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
class Deposits(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Deposit"
        plural_of = Deposit