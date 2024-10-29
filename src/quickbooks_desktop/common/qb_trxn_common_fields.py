
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin


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
class CreditCardTxnInfo:
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
class RefundAppliedToTxnAdd:
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

