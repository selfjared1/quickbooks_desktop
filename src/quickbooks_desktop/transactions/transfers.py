from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter,
)
from src.quickbooks_desktop.lists import (
    TransferFromAccountRef, TransferToAccountRef, ClassInQBRef,
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)

@dataclass
class TransferQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "TransferQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    modified_date_range_filter: Optional[ModifiedDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "ModifiedDateRangeFilter",
            "type": "Element",
        },
    )
    txn_date_range_filter: Optional[TxnDateRangeFilter] = field(
        default=None,
        metadata={
            "name": "TxnDateRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )


@dataclass
class TransferAdd(QBAddMixin):
    FIELD_ORDER = [
        "TxnDate", "TransferFromAccountRef", "TransferToAccountRef",
        "ClassRef", "Amount", "Memo"
    ]

    class Meta:
        name = "TransferAdd"

    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class TransferMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "TxnDate", "TransferFromAccountRef",
        "TransferToAccountRef", "ClassRef", "Amount", "Memo"
    ]

    class Meta:
        name = "TransferMod"

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "required": True,
            "max_length": 16,
        },
    )
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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
    
    
@dataclass
class Transfer(QBMixinWithQuery):
    
    class Meta:
        name = "Transfer"
    
    Query: Type[TransferQuery] = TransferQuery
    Add: Type[TransferAdd] = TransferAdd
    Mod: Type[TransferMod] = TransferMod
    
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
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    transfer_from_account_ref: Optional[TransferFromAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferFromAccountRef",
            "type": "Element",
        },
    )
    from_account_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FromAccountBalance",
            "type": "Element",
        },
    )
    transfer_to_account_ref: Optional[TransferToAccountRef] = field(
        default=None,
        metadata={
            "name": "TransferToAccountRef",
            "type": "Element",
        },
    )
    to_account_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ToAccountBalance",
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
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
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


@dataclass
class Transfers(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Transfer"
        plural_of = Transfer