from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin


@dataclass
class ParentRef(QBRefMixin):

    class Meta:
        name = "ParentRef"

VALID_TXN_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard", "BuildAssembly",
    "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo", "Deposit",
    "Estimate", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
    "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck", "PurchaseOrder",
    "ReceivePayment", "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck",
    "Transfer", "VendorCredit", "YTDAdjustment"
]

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
