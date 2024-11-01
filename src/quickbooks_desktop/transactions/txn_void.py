from dataclasses import dataclass, field
from typing import Optional
from src.quickbooks_desktop.mixins import QBMixin


@dataclass
class TxnVoid(QBMixin):
    FIELD_ORDER = [
        "TxnVoidType", "TxnID"
    ]

    class Meta:
        name = "TxnVoid"

    txn_void_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnVoidType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo",
                "Deposit", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
                "SalesReceipt", "VendorCredit"
            ],
        },
    )
    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )