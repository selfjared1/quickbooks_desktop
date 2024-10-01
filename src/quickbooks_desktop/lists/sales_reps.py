
from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Boolean

from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.qb_mixin import QBRefMixin, QBMixin

@dataclass
class SalesRepEntityRef(QBRefMixin):
    class Meta:
        name = "SalesRepEntityRef"

@dataclass
class SalesRepRef(QBRefMixin):
    class Meta:
        name = "SalesRepRef"


@dataclass
class SalesRep(QBMixin):
    class Meta:
        name = "sales_rep"

    __tablename__ = 'sales_rep'
    __sa_dataclass_metadata_key__ = 'sa'

    id: Optional[int] = field(
        init=False,
        metadata={'sa': Column(Integer, primary_key=True, autoincrement=True)}
    )
    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
            'sa': Column(String, unique=True)
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
            'sa': Column(DateTime)
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
            'sa': Column(DateTime)
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
            'sa': Column(String(16))
        },
    )
    initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial",
            "type": "Element",
            "max_length": 5,
            'sa': Column(String(5))
        },
    )
    is_active: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
            'sa': Column(Boolean)
        },
    )
    sales_rep_entity_ref: Optional[SalesRepEntityRef] = field(
        default=None,
        metadata={
            "name": "SalesRepEntityRef",
            "type": "Element",
            'sa': Column(String)
        },
    )