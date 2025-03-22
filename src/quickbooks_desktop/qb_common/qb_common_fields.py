from dataclasses import field
from typing import TypeVar, Optional, List

from _decimal import Decimal

TempVar = TypeVar('T')
list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
            "required": False,
        },
    )
list_ids: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
            "required": False,
        },
    )
full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 209,
            "required": False,
        },
    )
full_names: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
            "required": False,
        },
    )
amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": False,
        },
    )
