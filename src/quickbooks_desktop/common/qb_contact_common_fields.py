from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixin
from src.quickbooks_desktop.qb_special_fields import QBDates


@dataclass
class AdditionalContactRef(QBRefMixin):
    class Meta:
        name = "AdditionalContactRef"

    contact_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactName",
            "type": "Element",
            "required": True,
            "max_length": 40
        },
    )
    contact_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactValue",
            "type": "Element",
            "required": True,
            "max_length": 255
        },
    )

@dataclass
class AddressBlock(QBMixin):
    class Meta:
        name = "AddressBlock"

    addr1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr1",
            "type": "Element",
            "max_length": 41
        },
    )
    addr2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr2",
            "type": "Element",
            "max_length": 41
        },
    )
    addr3: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr3",
            "type": "Element",
            "max_length": 41
        },
    )
    addr4: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr4",
            "type": "Element",
            "max_length": 41
        },
    )
    addr5: Optional[str] = field(
        default=None,
        metadata={
            "name": "Addr5",
            "type": "Element",
            "max_length": 41
        },
    )

@dataclass
class BillAddressBlock(AddressBlock):
    class Meta:
        name = "BillAddressBlock"

@dataclass
class ShipAddressBlock(AddressBlock):
    class Meta:
        name = "ShipAddressBlock"

@dataclass
class Address(AddressBlock):
    class Meta:
        name = "Address"

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
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "max_length": 41
        },
    )

@dataclass
class EmployeeAddress(AddressBlock):
    class Meta:
        name = "EmployeeAddress"

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
class BillAddress(Address):
    class Meta:
        name = "BillAddress"

@dataclass
class ShipAddress(Address):
    class Meta:
        name = "ShipAddress"


@dataclass
class ShipToAddress(Address):
    class Meta:
        name = "ShipToAddress"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 41
        },
    )
    default_ship_to: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DefaultShipTo",
            "type": "Element"
        },
    )


@dataclass
class Contacts(QBMixin):
    class Meta:
        name = "Contacts"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element"
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
            "required": True
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
            "required": True
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16
        },
    )
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "max_length": 41
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "required": True,
            "max_length": 25
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 5
        },
    )

@dataclass
class AdditionalNotes(QBMixin):
    class Meta:
        name = "AdditionalNotes"

    note_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteID",
            "type": "Element",
            "required": True,
        },
    )
    date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "required": True,
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "Note",
            "type": "Element",
            "required": True,
            "max_length": 4095,
        },
    )

