from dataclasses import dataclass, field
from typing import Optional
from src.quickbooks_desktop.mixins import QBMixin



@dataclass
class TxnDel(QBMixin):
    FIELD_ORDER = [
        "TxnDelType", "TxnID"
    ]

    class Meta:
        name = "TxnDel"

    txn_del_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDelType",
            "type": "Element",
            "required": True,
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
                "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
                "ItemReceipt", "JournalEntry", "PurchaseOrder", "ReceivePayment", "SalesOrder",
                "SalesReceipt", "SalesTaxPaymentCheck", "TimeTracking", "TransferInventory",
                "VehicleMileage", "VendorCredit"
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