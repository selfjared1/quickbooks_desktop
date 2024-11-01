from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime, QBDateTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter,
    RefNumberFilter, RefNumberRangeFilter, ItemFilter,
)
from src.quickbooks_desktop.lists import (
    CustomerRef, ClassInQBRef, ItemRef, InventorySiteRef,
    InventorySiteLocationRef, AccountRef,
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin,
)


@dataclass
class SerialNumberAdjustment(QBMixin):

    class Meta:
        name = "SerialNumberAdjustment"

    add_serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AddSerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    remove_serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RemoveSerialNumber",
            "type": "Element",
            "max_length": 4095,
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )


@dataclass
class LotNumberAdjustment(QBMixin):

    class Meta:
        name = "LotNumberAdjustment"

    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    count_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "CountAdjustment",
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


@dataclass
class InventoryAdjustmentLineAdd(QBMixin):

    class Meta:
        name = "InventoryAdjustmentLineAdd"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
        },
    )
    quantity_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityAdjustment",
            "type": "Element",
        },
    )
    value_adjustment: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueAdjustment",
            "type": "Element",
        },
    )
    serial_number_adjustment: Optional[SerialNumberAdjustment] = field(
        default=None,
        metadata={
            "name": "SerialNumberAdjustment",
            "type": "Element",
        },
    )
    lot_number_adjustment: Optional[LotNumberAdjustment] = field(
        default=None,
        metadata={
            "name": "LotNumberAdjustment",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentLineMod(QBModMixin):

    class Meta:
        name = "InventoryAdjustmentLineMod"

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
    count_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "CountAdjustment",
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
    quantity_difference: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityDifference",
            "type": "Element",
        },
    )
    value_difference: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueDifference",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentLine(QBMixin):
    FIELD_ORDER = [
        "TxnLineID", "ItemRef", "SerialNumber", "SerialNumberAddedOrRemoved",
        "LotNumber", "InventorySiteLocationRef", "QuantityDifference", "ValueDifference"
    ]

    class Meta:
        name = "NameFilter"

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
            "required": True,
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
    serial_number_added_or_removed: Optional[str] = (
        field(
            default=None,
            metadata={
                "name": "SerialNumberAddedOrRemoved",
                "type": "Element",
                "valid_values": ["Added", "Removed"],
            },
        )
    )
    lot_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Element",
            "max_length": 40,
        },
    )
    inventory_site_location_ref: Optional[InventorySiteLocationRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteLocationRef",
            "type": "Element",
        },
    )
    quantity_difference: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityDifference",
            "type": "Element",
            "required": True,
        },
    )
    value_difference: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ValueDifference",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class InventoryAdjustmentQuery(QBQueryMixin):
    FIELD_ORDER = [
        "metaData", "iterator", "iteratorID", "TxnID", "RefNumber", "RefNumberCaseSensitive",
        "MaxReturned", "ModifiedDateRangeFilter", "TxnDateRangeFilter", "EntityFilter",
        "AccountFilter", "ItemFilter", "RefNumberFilter", "RefNumberRangeFilter",
        "IncludeLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "InventoryAdjustmentQuery"

    txn_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    ref_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumber",
            "type": "Element",
        },
    )
    ref_number_case_sensitive: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RefNumberCaseSensitive",
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
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
            "type": "Element",
        },
    )
    item_filter: Optional[ItemFilter] = field(
        default=None,
        metadata={
            "name": "ItemFilter",
            "type": "Element",
        },
    )
    ref_number_filter: Optional[RefNumberFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberFilter",
            "type": "Element",
        },
    )
    ref_number_range_filter: Optional[RefNumberRangeFilter] = field(
        default=None,
        metadata={
            "name": "RefNumberRangeFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustmentAdd(QBAddMixin):
    FIELD_ORDER = [
        "defMacro", "AccountRef", "TxnDate", "RefNumber", "InventorySiteRef",
        "CustomerRef", "ClassRef", "Memo", "ExternalGUID", "InventoryAdjustmentLineAdd"
    ]

    class Meta:
        name = "InventoryAdjustmentAdd"

    account_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
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
            "max_length": 11,
        },
    )
    inventory_site_ref: Optional[InventorySiteRef] = field(
        default=None,
        metadata={
            "name": "InventorySiteRef",
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    inventory_adjustment_line_add: List[InventoryAdjustmentLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineAdd",
            "type": "Element",
            "min_occurs": 1,
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
class InventoryAdjustmentMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "InventorySiteRef", "TxnDate",
        "RefNumber", "CustomerRef", "ClassRef", "Memo", "InventoryAdjustmentLineMod"
    ]

    class Meta:
        name = "InventoryAdjustmentMod"

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
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
            "max_length": 11,
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    inventory_adjustment_line_mod: List[InventoryAdjustmentLineMod] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineMod",
            "type": "Element",
        },
    )


@dataclass
class InventoryAdjustment(QBMixinWithQuery):

    class Meta:
        name = "InventoryAdjustment"
        
    Query: Type[InventoryAdjustmentQuery] = InventoryAdjustmentQuery
    Add: Type[InventoryAdjustmentAdd] = InventoryAdjustmentAdd
    Mod: Type[InventoryAdjustmentMod] = InventoryAdjustmentMod

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDateTime] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDateTime] = field(
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
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
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
            "max_length": 11,
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    inventory_adjustment_line_ret: List[InventoryAdjustmentLine] = field(
        default_factory=list,
        metadata={
            "name": "InventoryAdjustmentLineRet",
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
class InventoryAdjustments(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "InventoryAdjustment"
        plural_of = InventoryAdjustment
