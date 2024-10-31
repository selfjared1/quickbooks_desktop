
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin
from src.quickbooks_desktop.lists import (
    AccountRef, CustomerRef, ClassInQBRef, SalesTaxCodeRef, SalesRepRef, ItemRef,
    InventorySiteRef, InventorySiteLocationRef, OverrideItemAccountRef, ItemGroupRef,
    OverrideUomsetRef, DiscountAccountRef, DiscountClassRef
)
from src.quickbooks_desktop.common import LinkedTxn
from src.quickbooks_desktop.data_ext import DataExt


VALID_TXN_TYPE_VALUE = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
    "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
    "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
    "ItemReceipt", "JournalEntry", "LiabilityAdjustment", "Paycheck",
    "PayrollLiabilityCheck", "PurchaseOrder", "ReceivePayment", "SalesOrder",
    "SalesReceipt", "SalesTaxPaymentCheck", "Transfer", "VendorCredit", "YTDAdjustment"
]

@dataclass
class PayeeEntityRef(QBRefMixin):
    class Meta:
        name = "PayeeEntityRef"

@dataclass
class CreditCardTxnInputInfo(QBMixin):

    class Meta:
        name = "CreditCardTxnInputInfo"

    credit_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardNumber",
            "type": "Element",
            "required": True,
            "max_length": 25,
        },
    )
    expiration_month: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationMonth",
            "type": "Element",
            "required": True,
            "valid_values": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        },
    )
    expiration_year: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExpirationYear",
            "type": "Element",
            "required": True,
        },
    )
    name_on_card: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCard",
            "type": "Element",
            "required": True,
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
            "max_length": 18,
        },
    )
    commercial_card_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CommercialCardCode",
            "type": "Element",
            "max_length": 24,
        },
    )
    transaction_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionMode",
            "type": "Element",
            "valid_values": ["CardNotPresent", "CardPresent"]
        },
    )
    credit_card_txn_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnType",
            "type": "Element",
            "valid_values": ["Authorization", "Capture", "Charge", "Refund", "VoiceAuthorization"]
        },
    )


@dataclass
class CreditCardTxnResultInfo(QBMixin):

    class Meta:
        name = "CreditCardTxnResultInfo"

    result_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "ResultCode",
            "type": "Element",
            "required": True,
        },
    )
    result_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultMessage",
            "type": "Element",
            "required": True,
            "max_length": 60,
        },
    )
    credit_card_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditCardTransID",
            "type": "Element",
            "required": True,
            "max_length": 24,
        },
    )
    merchant_account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "MerchantAccountNumber",
            "type": "Element",
            "required": True,
            "max_length": 32,
        },
    )
    authorization_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuthorizationCode",
            "type": "Element",
            "max_length": 12,
        },
    )
    avsstreet: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSStreet",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    avszip: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVSZip",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    card_security_code_match: Optional[str] = field(
        default=None,
        metadata={
            "name": "CardSecurityCodeMatch",
            "type": "Element",
            "valid_values": ["Pass", "Fail", "NotAvailable"],
        },
    )
    recon_batch_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReconBatchID",
            "type": "Element",
            "max_length": 84,
        },
    )
    payment_grouping_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "PaymentGroupingCode",
            "type": "Element",
        },
    )
    payment_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentStatus",
            "type": "Element",
            "required": True,
            "valid_values": ["Unknown", "Completed"],
        },
    )
    txn_authorization_time: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationTime",
            "type": "Element",
            "required": True,
        },
    )
    txn_authorization_stamp: Optional[int] = field(
        default=None,
        metadata={
            "name": "TxnAuthorizationStamp",
            "type": "Element",
        },
    )
    client_trans_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientTransID",
            "type": "Element",
            "max_length": 16,
        },
    )


@dataclass
class CreditCardTxnInfo(QBMixin):
    class Meta:
        name = "CreditCardTxnInfo"

    credit_card_txn_input_info: Optional[CreditCardTxnInputInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnInputInfo",
            "type": "Element",
            "required": True,
        },
    )
    credit_card_txn_result_info: Optional[CreditCardTxnResultInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardTxnResultInfo",
            "type": "Element",
            "required": True,
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
class SetCreditCreditTxnId(QBMixin):
    class Meta:
        name = "SetCreditCreditTxnId"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 36,
        },
    )
    use_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "useMacro",
            "type": "Attribute",
        },
    )


@dataclass
class SetCredit(QBMixin):

    class Meta:
        name = "SetCredit"

    credit_txn_id: Optional[SetCreditCreditTxnId] = field(
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
class AppliedToTxnAdd(QBMixin):
    FIELD_ORDER = [
        "TxnID", "PaymentAmount", "SetCredit", "DiscountAmount",
        "DiscountAccountRef", "DiscountClassRef"
    ]

    class Meta:
        name = "AppliedToTxnAdd"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    payment_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PaymentAmount",
            "type": "Element",
        },
    )
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )


@dataclass
class AppliedToTxnMod(QBMixin):
    FIELD_ORDER = [
        "TxnID", "PaymentAmount", "SetCredit", "DiscountAmount",
        "DiscountAccountRef", "DiscountClassRef"
    ]

    class Meta:
        name = "AppliedToTxnMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    payment_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PaymentAmount",
            "type": "Element",
        },
    )
    set_credit: List[SetCredit] = field(
        default_factory=list,
        metadata={
            "name": "SetCredit",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )


@dataclass
class AppliedToTxn(QBMixin):
    FIELD_ORDER = [
        "TxnID", "TxnType", "TxnDate", "RefNumber", "BalanceRemaining",
        "Amount", "DiscountAmount", "DiscountAccountRef",
        "DiscountClassRef", "LinkedTxn"
    ]

    class Meta:
        name = "AppliedToTxn"

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
            "valid_values": VALID_TXN_TYPE_VALUE
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
    balance_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
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
    txn_line_detail: List[TxnLineDetail] = field(
        default_factory=list,
        metadata={
            "name": "TxnLineDetail",
            "type": "Element",
        },
    )
    discount_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
        },
    )
    discount_account_ref: Optional[DiscountAccountRef] = field(
        default=None,
        metadata={
            "name": "DiscountAccountRef",
            "type": "Element",
        },
    )
    discount_class_ref: Optional[DiscountClassRef] = field(
        default=None,
        metadata={
            "name": "DiscountClassRef",
            "type": "Element",
        },
    )
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )


@dataclass
class RefundAppliedToTxnAdd(QBMixin):
    class Meta:
        name = "RefundAppliedToTxnAdd"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    refund_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RefundAmount",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class RefundAppliedToTxn(QBMixin):
    class Meta:
        name = "RefundAppliedToTxnAdd"

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
            "valid_values": [
                "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
                "BuildAssembly", "Charge", "Check", "CreditCardCharge",
                "CreditCardCredit", "CreditMemo", "Deposit", "Estimate",
                "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
                "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck",
                "PurchaseOrder", "ReceivePayment", "SalesOrder", "SalesReceipt",
                "SalesTaxPaymentCheck", "Transfer", "VendorCredit", "YTDAdjustment"
            ],
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
    credit_remaining: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemaining",
            "type": "Element",
            "required": True,
        },
    )
    refund_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RefundAmount",
            "type": "Element",
            "required": True,
        },
    )
    credit_remaining_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditRemainingInHomeCurrency",
            "type": "Element",
        },
    )
    refund_amount_in_home_currency: Optional[Decimal] = (
        field(
            default=None,
            metadata={
                "name": "RefundAmountInHomeCurrency",
                "type": "Element",
            },
        )
    )

@dataclass
class LinkToTxn(QBMixin):
    FIELD_ORDER = [
        "TxnID", "TxnLineID"
    ]

    class Meta:
        name = "LinkToTxn"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
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


@dataclass
class ExpenseLineAdd(QBMixin):
    FIELD_ORDER = [
        "AccountRef", "Amount", "Memo", "CustomerRef",
        "ClassRef", "BillableStatus", "SalesRepRef", "DataExt"
    ]

    class Meta:
        name = "ExpenseLineAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
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
class ItemLineAdd(QBMixin):
    FIELD_ORDER = [
        "ItemRef", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "Desc", "Quantity",
        "UnitOfMeasure", "Cost", "Amount", "CustomerRef",
        "ClassRef", "BillableStatus", "OverrideItemAccountRef",
        "LinkToTxn", "SalesRepRef", "DataExt"
    ]

    class Meta:
        name = "ItemLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
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
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    link_to_txn: Optional[LinkToTxn] = field(
        default=None,
        metadata={
            "name": "LinkToTxn",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )

@dataclass
class ItemGroupLineAdd(QBMixin):
    FIELD_ORDER = [
        "ItemGroupRef", "Quantity", "UnitOfMeasure", "InventorySiteRef",
        "InventorySiteLocationRef", "DataExt"
    ]

    class Meta:
        name = "ItemGroupLineAdd"

    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )

@dataclass
class ExpenseLineMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "AccountRef", "Amount", "Memo",
        "CustomerRef", "ClassRef", "BillableStatus", "SalesRepRef"
    ]

    class Meta:
        name = "ExpenseLineMod"

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
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )


@dataclass
class ItemLineMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "InventorySiteRef", "InventorySiteLocationRef",
        "SerialNumber", "LotNumber", "Desc", "Quantity",
        "UnitOfMeasure", "OverrideUOMSetRef", "Cost", "Amount",
        "CustomerRef", "ClassRef", "BillableStatus", "OverrideItemAccountRef",
        "SalesRepRef"
    ]

    class Meta:
        name = "ItemLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
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
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    override_item_account_ref: Optional[OverrideItemAccountRef] = field(
        default=None,
        metadata={
            "name": "OverrideItemAccountRef",
            "type": "Element",
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupLineMod(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemGroupRef", "Quantity", "UnitOfMeasure",
        "OverrideUOMSetRef", "ItemLineMod"
    ]

    class Meta:
        name = "ItemGroupLineMod"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )

@dataclass
class ExpenseLine(QBMixin):

    class Meta:
        name = "ExpenseLine"

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
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
class ItemLine(QBMixin):

    class Meta:
        name = "ItemLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
            "type": "Element",
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Cost",
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
    tax_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    billable_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillableStatus",
            "type": "Element",
            "valid_values": ["Billable", "NotBillable", "HasBeenBilled"],
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
class ItemGroupLine(QBMixin):

    class Meta:
        name = "ItemGroupLine"

    txn_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnLineID",
            "type": "Element",
            "required": True,
        },
    )
    item_group_ref: Optional[ItemGroupRef] = field(
        default=None,
        metadata={
            "name": "ItemGroupRef",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )
    override_uomset_ref: Optional[OverrideUomsetRef] = field(
        default=None,
        metadata={
            "name": "OverrideUOMSetRef",
            "type": "Element",
        },
    )
    total_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalAmount",
            "type": "Element",
            "required": True,
        },
    )
    item_line_ret: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    data_ext: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExt",
            "type": "Element",
        },
    )

@dataclass
class DiscountLineAdd(QBMixin):

    class Meta:
        name = "DiscountLineAdd"

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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

@dataclass
class DiscountLine(QBMixin):

    class Meta:
        name = "DiscountLine"

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )
    is_taxable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxable",
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