from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from src.quickbooks_desktop.mixins.qb_mixins import ToXmlMixin, QBRefMixin
from decimal import Decimal


class MatchCriterionValue(Enum):
    STARTS_WITH = "StartsWith"
    CONTAINS = "Contains"
    ENDS_WITH = "EndsWith"

@dataclass
class MatchCriterion:
    value: Optional[MatchCriterionValue] = field(default=None)

class OperatorValue(Enum):
    LESS_THAN = "LessThan"
    LESS_THAN_EQUAL = "LessThanEqual"
    EQUAL = "Equal"
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_EQUAL = "GreaterThanEqual"

@dataclass
class Operator:
    value: Optional[OperatorValue] = field(default=None)

@dataclass
class CurrencyFilter(QBRefMixin):
    # I know it doesn't set Ref in the name but it's a Ref
    class Meta:
        name = "CurrencyFilter"

@dataclass
class NameFilter(ToXmlMixin):
    match_criterion: Optional[MatchCriterion] = field(
        default=None,
        metadata={
            "name": "MatchCriterion",
            "type": "Element",
            "required": True,
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

@dataclass
class TotalBalanceFilter:
    operator: Optional[Operator] = field(
        default=None,
        metadata={
            "name": "Operator",
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
class ClassFilter:
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