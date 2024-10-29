from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.common import AddressBlock
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin, PluralListSaveMixin
from src.quickbooks_desktop.common.qb_query_common_fields import NameFilter, NameRangeFilter


@dataclass
class InventorySiteRef(QBRefMixin):

    class Meta:
        name = "InventorySiteRef"

@dataclass
class ParentSiteRef(QBRefMixin):

    class Meta:
        name = "ParentSiteRef"

@dataclass
class InventorySiteLocationRef(QBRefMixin):

    class Meta:
        name = "InventorySiteLocationRef"

@dataclass
class SiteAddress(AddressBlock):
    class Meta:
        name = "SiteAddress"

    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "max_length": 31
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "max_length": 21
        },
    )
    postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "max_length": 13
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "max_length": 31
        },
    )

@dataclass
class SiteAddressBlock(AddressBlock):
    class Meta:
        name = "SiteAddressBlock"

@dataclass
class InventorySiteQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "ActiveStatus", "FromModifiedDate", "ToModifiedDate",
        "NameFilter", "NameRangeFilter", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteQuery"

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


@dataclass
class InventorySiteAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ParentSiteRef", "SiteDesc", "Contact", "Phone",
        "Fax", "Email", "SiteAddress", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteAdd"

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
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )

@dataclass
class InventorySiteMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ParentSiteRef", "SiteDesc",
        "Contact", "Phone", "Fax", "Email", "SiteAddress", "IncludeRetElement"
    ]

    class Meta:
        name = "InventorySiteMod"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )


@dataclass
class InventorySite(QBMixinWithQuery):

    class Meta:
        name = "InventorySite"

    Query: Type[InventorySiteQuery] = InventorySiteQuery
    Add: Type[InventorySiteAdd] = InventorySiteAdd
    Mod: Type[InventorySiteMod] = InventorySiteMod

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
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
    parent_site_ref: Optional[ParentSiteRef] = field(
        default=None,
        metadata={
            "name": "ParentSiteRef",
            "type": "Element",
        },
    )
    is_default_site: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsDefaultSite",
            "type": "Element",
        },
    )
    site_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SiteDesc",
            "type": "Element",
            "max_length": 100,
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    site_address: Optional[SiteAddress] = field(
        default=None,
        metadata={
            "name": "SiteAddress",
            "type": "Element",
        },
    )
    site_address_block: Optional[SiteAddressBlock] = field(
        default=None,
        metadata={
            "name": "SiteAddressBlock",
            "type": "Element",
        },
    )

class InventorySites(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "InventorySite"
        plural_of = InventorySite