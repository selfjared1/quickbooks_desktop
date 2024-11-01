from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    LinkedTxn, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, SetCredit,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter,
)
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, ItemSalesTaxRef, TemplateRef, CustomerRef, ClassInQBRef, CurrencyRef, TermsRef,
    SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef, ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PriceLevelRef,
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)



@dataclass
class TxnDel(QBMixin):
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