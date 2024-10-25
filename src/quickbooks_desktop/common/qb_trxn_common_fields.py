
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin


@dataclass
class CreditCardTxnInputInfo:
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