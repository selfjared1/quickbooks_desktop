
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type, Dict
from collections import defaultdict

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    LinkedTxn, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, SetCredit,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter
)
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, ItemSalesTaxRef, TemplateRef, CustomerRef, QBClassRef, AraccountRef, CurrencyRef, TermsRef,
    SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef, ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PriceLevelRef, OverrideItemAccountRef, AccountRef, PaymentMethodRef, DepositToAccountRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBRefMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin, SaveMixin
)

@dataclass
class ReceivePaymentRet:
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
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
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
            "max_length": 20,
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
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    unused_payment: Optional[UnusedPayment] = field(
        default=None,
        metadata={
            "name": "UnusedPayment",
            "type": "Element",
        },
    )
    unused_credits: Optional[UnusedCredits] = field(
        default=None,
        metadata={
            "name": "UnusedCredits",
            "type": "Element",
        },
    )
    external_guid: Optional[ExternalGuid] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    applied_to_txn_ret: List[AppliedToTxnRet] = field(
        default_factory=list,
        metadata={
            "name": "AppliedToTxnRet",
            "type": "Element",
        },
    )
    data_ext_ret: List[DataExtRet] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )