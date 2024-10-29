from dataclasses import dataclass, field
from typing import Optional, List, Type

from src.quickbooks_desktop.mixins import QBMixin, QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBAddMixin, PluralMixin
from src.quickbooks_desktop.common import NameFilter, NameRangeFilter
from src.quickbooks_desktop.qb_special_fields import QBDates, QBPriceType


@dataclass
class OverrideUomsetRef(QBRefMixin):

    class Meta:
        name = "OverrideUomsetRef"


@dataclass
class DefaultUnit(QBMixin):

    class Meta:
        name = "DefaultUnit"

    unit_used_for: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitUsedFor",
            "type": "Element",
            "required": True,
            "valid_values": ["Purchase", "Sales", "Shipping"]
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )


@dataclass
class BaseUnit(QBMixin):

    class Meta:
        name = "BaseUnit"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )


@dataclass
class RelatedUnit(QBMixin):

    class Meta:
        name = "RelatedUnit"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    conversion_ratio: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "ConversionRatio",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UnitOfMeasureSetQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "UnitOfMeasureSetQuery"

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
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
            "valid_values": ["ActiveOnly", "InactiveOnly", "All"],
        },
    )
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
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    meta_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaData",
            "type": "Attribute",
            "valid_values": ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"],
        },
    )


@dataclass
class UnitOfMeasureSetAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "UnitOfMeasureType", "BaseUnit",
        "RelatedUnit", "DefaultUnit"
    ]

    class Meta:
        name = "UnitOfMeasureSetAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    unit_of_measure_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureType",
            "type": "Element",
            "required": True,
            "valid_values": ["Area", "Count", "Length", "Other", "Time", "Volume", "Weight"],
        },
    )
    base_unit: Optional[BaseUnit] = field(
        default=None,
        metadata={
            "name": "BaseUnit",
            "type": "Element",
            "required": True,
        },
    )
    related_unit: List[RelatedUnit] = field(
        default_factory=list,
        metadata={
            "name": "RelatedUnit",
            "type": "Element",
        },
    )
    default_unit: List[DefaultUnit] = field(
        default_factory=list,
        metadata={
            "name": "DefaultUnit",
            "type": "Element",
        },
    )


@dataclass
class UnitOfMeasureSet(QBMixinWithQuery):

    class Meta:
        name = "Unit Of Measure Set"

    Query: Type[UnitOfMeasureSetQuery] = UnitOfMeasureSetQuery
    Add: Type[UnitOfMeasureSetAdd] = UnitOfMeasureSetAdd
    # No Mod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    unit_of_measure_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureType",
            "type": "Element",
            "valid_values": ["Area", "Count", "Length", "Other", "Time", "Volume", "Weight"]
        },
    )
    base_unit: Optional[BaseUnit] = field(
        default=None,
        metadata={
            "name": "BaseUnit",
            "type": "Element",
        },
    )
    related_unit: List[RelatedUnit] = field(
        default_factory=list,
        metadata={
            "name": "RelatedUnit",
            "type": "Element",
        },
    )
    default_unit: List[DefaultUnit] = field(
        default_factory=list,
        metadata={
            "name": "DefaultUnit",
            "type": "Element",
        },
    )


@dataclass
class UnitOfMeasureSets(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "UnitOfMeasureSet"
        plural_of = UnitOfMeasureSet