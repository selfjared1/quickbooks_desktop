from dataclasses import dataclass, field
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter, RefNumberFilter, RefNumberRangeFilter,
    ItemFilter,
)
from src.quickbooks_desktop.lists import (
    ItemInventoryAssemblyRef, ItemRef, InventorySiteRef, InventorySiteLocationRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class ComponentItemLine:

    class Meta:
        name = "ComponentItemLine"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
            "required": True,
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
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    quantity_needed: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityNeeded",
            "type": "Element",
        },
    )


@dataclass
class BuildAssemblyQuery(QBQueryMixin):
    FIELD_ORDER = [
        "TxnID", "RefNumber", "RefNumberCaseSensitive", "MaxReturned",
        "ModifiedDateRangeFilter", "TxnDateRangeFilter", "ItemFilter",
        "RefNumberFilter", "RefNumberRangeFilter", "PendingStatus",
        "IncludeComponentLineItems", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "BuildAssemblyQuery"

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
    pending_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "PendingStatus",
            "type": "Element",
            "valid_values": ["All", "PendingOnly", "NotPendingOnly"],
        },
    )
    include_component_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeComponentLineItems",
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
class BuildAssemblyAdd(QBAddMixin):
    FIELD_ORDER = [
        "ItemInventoryAssemblyRef", "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "TxnDate", "RefNumber", "Memo", "QuantityToBuild", "MarkPendingIfRequired",
        "ExternalGUID"
    ]

    class Meta:
        name = "BuildAssemblyAdd"

    item_inventory_assembly_ref: Optional[ItemInventoryAssemblyRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryAssemblyRef",
            "type": "Element",
            "required": True,
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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
            "required": True,
        },
    )
    mark_pending_if_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MarkPendingIfRequired",
            "type": "Element",
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )


@dataclass
class BuildAssemblyMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "InventorySiteRef", "InventorySiteLocationRef", "SerialNumber",
        "LotNumber", "TxnDate", "RefNumber", "Memo", "QuantityToBuild", "MarkPendingIfRequired",
        "RemovePending"
    ]

    class Meta:
        name = "BuildAssemblyMod"

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
    memo: Optional[str] = field(
        default=None,
        metadata={
            "name": "Memo",
            "type": "Element",
            "max_length": 4095,
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
        },
    )
    mark_pending_if_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MarkPendingIfRequired",
            "type": "Element",
        },
    )
    remove_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RemovePending",
            "type": "Element",
        },
    )


@dataclass
class BuildAssembly(QBMixinWithQuery):
    
    class Meta:
        name = "BuildAssembly"

    Query: Type[BuildAssemblyQuery] = BuildAssemblyQuery
    Add: Type[BuildAssemblyAdd] = BuildAssemblyAdd
    Mod: Type[BuildAssemblyMod] = BuildAssemblyMod
    
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
    item_inventory_assembly_ref: Optional[ItemInventoryAssemblyRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryAssemblyRef",
            "type": "Element",
            "required": True,
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
            "max_length": 11,
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
    is_pending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    quantity_to_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityToBuild",
            "type": "Element",
            "required": True,
        },
    )
    quantity_can_build: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityCanBuild",
            "type": "Element",
            "required": True,
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
            "required": True,
        },
    )
    quantity_on_sales_order: Optional[int] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
            "type": "Element",
            "required": True,
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    component_item_line_ret: List[ComponentItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ComponentItemLineRet",
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
class BuildAssemblies(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "BuildAssembly"
        plural_of = BuildAssembly
