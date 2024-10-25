from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from src.quickbooks_desktop.mixins.qb_mixins import ToXmlMixin, QBRefMixin
from src.quickbooks_desktop.qb_special_fields import QBDates
from decimal import Decimal



@dataclass
class CurrencyFilter(QBRefMixin):
    # I know it doesn't set Ref in the name but it's a Ref
    class Meta:
        name = "CurrencyFilter"

@dataclass
class NameFilter(ToXmlMixin):
    match_criterion: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatchCriterion",
            "type": "Element",
            "required": True,
            "valid_values": ["StartsWith", "Contains", "EndsWith"]

        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class NameRangeFilter(ToXmlMixin):
    from_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FromName",
            "type": "Element",
        },
    )
    to_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToName",
            "type": "Element",
        },
    )

VALID_OPERATOR_VALUES = ["LessThan", "LessThanEqual", "Equal", "GreaterThan", "GreaterThanEqual"]


@dataclass
class TotalBalanceFilter(ToXmlMixin):
    operator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Element",
            "required": True,
            "valid_values": VALID_OPERATOR_VALUES
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
class ClassFilter(ToXmlMixin):
    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
        },
    )
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class ModifiedDateRangeFilter(ToXmlMixin):
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )

@dataclass
class TxnDateRangeFilter(ToXmlMixin):
    from_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromTxnDate",
            "type": "Element",
        },
    )
    to_txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToTxnDate",
            "type": "Element",
        },
    )
    date_macro: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "DateMacro",
            "type": "Element",
        },
    )

    def __post_init__(self):
        # Validate that from_txn_date and to_txn_date have date_is_macro as False
        if self.from_txn_date and self.from_txn_date.date_is_macro:
            raise ValueError("from_txn_date cannot be a macro date.")

        if self.to_txn_date and self.to_txn_date.date_is_macro:
            raise ValueError("to_txn_date cannot be a macro date.")

        # Validate that date_macro has date_is_macro as True
        if self.date_macro and not self.date_macro.date_is_macro:
            raise ValueError("date_macro must be a macro date.")


@dataclass
class EntityFilter(ToXmlMixin):

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
        },
    )
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class AccountFilter(ToXmlMixin):

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
        },
    )
    list_idwith_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListIDWithChildren",
            "type": "Element",
        },
    )
    full_name_with_children: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullNameWithChildren",
            "type": "Element",
        },
    )

@dataclass
class RefNumberFilter(ToXmlMixin):

    match_criterion: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatchCriterion",
            "type": "Element",
            "required": True,
            "valid_values": ["StartsWith", "Contains", "EndsWith"]
        },
    )
    ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefNumber",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class RefNumberRangeFilter(ToXmlMixin):
    from_ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "FromRefNumber",
            "type": "Element",
        },
    )
    to_ref_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToRefNumber",
            "type": "Element",
        },
    )