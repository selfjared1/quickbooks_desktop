from dataclasses import dataclass, field
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBAddMixin, QBModMixin
)

from src.quickbooks_desktop.common import (OtherNameAddress, OtherNameAddressBlock,
    NameFilter, NameRangeFilter
)



@dataclass
class OtherNameRef(QBRefMixin):
    class Meta:
        name = "OtherNameRef"



@dataclass
class OtherNameQuery(QBQueryMixin):

    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "OtherNameQuery"

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
    active_status: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )

@dataclass
class OtherNameAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "CompanyName", "Salutation", "FirstName",
        "MiddleName", "LastName", "OtherNameAddress", "Phone",
        "AltPhone", "Fax", "Email", "Contact", "AltContact",
        "AccountNumber", "Notes", "ExternalGUID"
    ]

    class Meta:
        name = "OtherNameAdd"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
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
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
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
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
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

@dataclass
class OtherNameMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "CompanyName",
        "Salutation", "FirstName", "MiddleName", "LastName",
        "OtherNameAddress", "Phone", "AltPhone", "Fax", "Email",
        "Contact", "AltContact", "AccountNumber", "Notes"
    ]

    class Meta:
        name = "OtherNameMod"

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
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
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
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
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
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )


@dataclass
class OtherName(QBMixinWithQuery):
    class Meta:
        name = "OtherName"

    Query: Type[OtherNameQuery] = OtherNameQuery
    Add: Type[OtherNameAdd] = OtherNameAdd
    Mod: Type[OtherNameMod] = OtherNameMod

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
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Element",
            "max_length": 41,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    other_name_address: Optional[OtherNameAddress] = field(
        default=None,
        metadata={
            "name": "OtherNameAddress",
            "type": "Element",
        },
    )
    other_name_address_block: Optional[OtherNameAddressBlock] = field(
        default=None,
        metadata={
            "name": "OtherNameAddressBlock",
            "type": "Element",
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
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
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
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41,
        },
    )
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


class OtherNames(PluralMixin):

    class Meta:
        name = "OtherName"
        plural_of = OtherName



