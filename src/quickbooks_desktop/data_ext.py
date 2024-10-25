from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBAddMixin, QBModMixin, QBMixin
)
from src.quickbooks_desktop.lists import (
    ClassInQBRef, SalesRepRef, TermsRef, SalesTaxCodeRef, ItemSalesTaxRef, PriceLevelRef, CurrencyRef,
)

from src.quickbooks_desktop.common import (
    ParentRef, NameFilter, NameRangeFilter, TotalBalanceFilter, CurrencyFilter, Contacts,
    ClassFilter, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, ShipToAddress,
    AdditionalContactRef, PreferredPaymentMethodRef, CreditCardInfo, JobTypeRef, AdditionalNotes,
    ContactsMod, AdditionalNotesMod, AdditionalNotesRet, ListObjRef
)

VALID_TXN_DATA_EXT_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
    "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
    "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
    "ItemReceipt", "JournalEntry", "PurchaseOrder", "ReceivePayment",
    "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck", "VendorCredit"
]

VALID_LIST_DATA_EXT_TYPE_VALUES = ["Account", "Customer", "Employee", "Item", "OtherName", "Vendor"]

@dataclass
class DataExtAdd(QBAddMixin):
    FIELD_ORDER = [
        "OwnerID", "DataExtName", "ListDataExtType", "ListObjRef",
        "TxnDataExtType", "TxnID", "TxnLineID", "OtherDataExtType", "DataExtValue"
    ]

    class Meta:
        name = "DataExtAdd"

    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
            "required": True,
        },
    )
    data_ext_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtName",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    list_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListDataExtType",
            "type": "Element",
            "valid_values": ["Account", "Customer", "Employee", "Item", "OtherName", "Vendor"]
        },
    )
    list_obj_ref: Optional[ListObjRef] = field(
        default=None,
        metadata={
            "name": "ListObjRef",
            "type": "Element",
        },
    )
    txn_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDataExtType",
            "type": "Element",
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES,
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
    other_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherDataExtType",
            "type": "Element",
            "valid_values": ["Company"]
        },
    )
    data_ext_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtValue",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class DataExtMod(QBAddMixin):
    FIELD_ORDER = [
        "OwnerID", "DataExtName", "ListDataExtType", "ListObjRef",
        "TxnDataExtType", "TxnID", "TxnLineID", "OtherDataExtType", "DataExtValue"
    ]

    class Meta:
        name = "DataExtMod"

    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
            "required": True,
        },
    )
    data_ext_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtName",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    list_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListDataExtType",
            "type": "Element",
            "valid_values": VALID_LIST_DATA_EXT_TYPE_VALUES
        },
    )
    list_obj_ref: Optional[ListObjRef] = field(
        default=None,
        metadata={
            "name": "ListObjRef",
            "type": "Element",
        },
    )
    txn_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnDataExtType",
            "type": "Element",
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES,
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
    other_data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherDataExtType",
            "type": "Element",
            "valid_values": ["Company"]
        },
    )
    data_ext_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtValue",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class DataExt(QBMixin):

    class Meta:
        name = "DataExtRet"

    #There is no Query
    Add: Type[DataExtAdd] = DataExtAdd
    Mod: Type[DataExtMod] = DataExtMod

    owner_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    data_ext_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtName",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    data_ext_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtType",
            "type": "Element",
            "required": True,
            "valid_values": VALID_TXN_DATA_EXT_TYPE_VALUES + VALID_LIST_DATA_EXT_TYPE_VALUES + ["Company"],
        },
    )
    data_ext_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtValue",
            "type": "Element",
            "required": True,
        },
    )