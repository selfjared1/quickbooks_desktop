from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List

from src.quickbooks_desktop.mixins import QBMixin
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin




VALID_TXN_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard", "BuildAssembly",
    "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo", "Deposit",
    "Estimate", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
    "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck", "PurchaseOrder",
    "ReceivePayment", "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck",
    "Transfer", "VendorCredit", "YTDAdjustment"
]

@dataclass
class ParentRef(QBRefMixin):

    class Meta:
        name = "ParentRef"


@dataclass
class ListObjRef(QBRefMixin):

    class Meta:
        name = "ListObjRef"


@dataclass
class SalesTaxReturnLineRef(QBRefMixin):

    class Meta:
        name = "SalesTaxReturnLineRef"


@dataclass
class PreferredPaymentMethodRef(QBRefMixin):

    class Meta:
        name = "PreferredPaymentMethodRef"

@dataclass
class JobTypeRef(QBRefMixin):

    class Meta:
        name = "JobTypeRef"

@dataclass
class CreditCardInfo(QBMixin):
    FIELD_ORDER = [
        "CreditCardNumber", "ExpirationMonth", "ExpirationYear", "NameOnCard",
        "CreditCardAddress", "CreditCardPostalCode"
    ]

    class Meta:
        name = "CreditCardInfo"

    credit_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    expiration_month: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationMonth",
            "type": "Element",
            "valid_values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        },
    )
    expiration_year: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationYear",
            "type": "Element",
        },
    )
    name_on_card: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCard",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardAddress",
            "type": "Element",
            "max_length": 41,
        },
    )
    credit_card_postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardPostalCode",
            "type": "Element",
            "max_length": 41,
        },
    )

@dataclass
class TxnLineDetail(QBMixin):
    class Meta:
        name = "TxnLineDetail"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class SetCredit(QBMixin):

    class Meta:
        name = "SetCredit"

    credit_txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditTxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
        },
    )
    applied_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
            "required": True,
        },
    )
    override: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Override",
            "type": "Element",
        },
    )

@dataclass
class LinkedTxn(QBMixin):

    class Meta:
        name = "LinkedTxn"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnType",
            "type": "Element",
            "required": True,
            "valid_values": VALID_TXN_TYPE_VALUES,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
            "required": True,
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
    link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "LinkType",
            "type": "Element",
            "valid_values": ["AMTTYPE", "QUANTYPE"]
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": True,
        },
    )
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )

