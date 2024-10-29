from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin
)
from src.quickbooks_desktop.common import (
    ParentRef, NameFilter, NameRangeFilter, TotalBalanceFilter, CurrencyFilter, Contacts,
    ClassFilter, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, ShipToAddress,
    AdditionalContactRef, PreferredPaymentMethodRef, CreditCardInfo, JobTypeRef, AdditionalNotes,
    ContactsMod, AdditionalNotesMod, AdditionalNotesRet, VendorAddress, VendorAddressBlock,
)
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, CurrencyRef, ClassInQBRef, VendorTypeRef, TermsRef, BillingRateRef, PrefillAccountRef
)
from src.quickbooks_desktop.data_ext import DataExt

@dataclass
class PrefVendorRef(QBRefMixin):
    class Meta:
        name = "PrefVendorRef"

@dataclass
class TaxVendorRef(QBRefMixin):
    class Meta:
        name = "TaxVendorRef"

@dataclass
class VendorQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "TotalBalanceFilter", "CurrencyFilter",
        "ClassFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "VendorQuery"

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
    total_balance_filter: Optional[TotalBalanceFilter] = field(
        default=None,
        metadata={
            "name": "TotalBalanceFilter",
            "type": "Element",
        },
    )
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
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
class VendorAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ClassRef", "CompanyName", "Salutation",
        "FirstName", "MiddleName", "LastName", "JobTitle", "VendorAddress",
        "ShipAddress", "Phone", "AltPhone", "Fax", "Email",
        "Cc", "Contact", "AltContact", "AdditionalContactRef",
        "Contacts", "NameOnCheck", "AccountNumber", "Notes",
        "AdditionalNotes", "VendorTypeRef", "TermsRef", "CreditLimit",
        "VendorTaxIdent", "IsVendorEligibleFor1099", "OpenBalance",
        "OpenBalanceDate", "BillingRateRef", "ExternalGUID",
        "PrefillAccountRef", "CurrencyRef"
    ]

    class Meta:
        name = "VendorAdd"

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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
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
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
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
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
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
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
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
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
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
    additional_notes: List[AdditionalNotes] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotes",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    open_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "OpenBalance",
            "type": "Element",
        },
    )
    open_balance_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OpenBalanceDate",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
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
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class VendorMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ClassRef",
        "CompanyName", "Salutation", "FirstName", "MiddleName",
        "LastName", "JobTitle", "VendorAddress", "ShipAddress",
        "Phone", "AltPhone", "Fax", "Email", "Cc", "Contact",
        "AltContact", "AdditionalContactRef", "ContactsMod",
        "NameOnCheck", "AccountNumber", "Notes", "AdditionalNotesMod",
        "VendorTypeRef", "TermsRef", "CreditLimit", "VendorTaxIdent",
        "IsVendorEligibleFor1099", "BillingRateRef", "PrefillAccountRef",
        "CurrencyRef"
    ]

    class Meta:
        name = "VendorMod"


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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
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
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
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
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
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
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
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
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts_mod: List[ContactsMod] = field(
        default_factory=list,
        metadata={
            "name": "ContactsMod",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
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
    additional_notes_mod: List[AdditionalNotesMod] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesMod",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class Vendor(QBMixinWithQuery):

    class Meta:
        name = "Vendor"

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
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    is_tax_agency: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxAgency",
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
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    vendor_address: Optional[VendorAddress] = field(
        default=None,
        metadata={
            "name": "VendorAddress",
            "type": "Element",
        },
    )
    vendor_address_block: Optional[VendorAddressBlock] = field(
        default=None,
        metadata={
            "name": "VendorAddressBlock",
            "type": "Element",
        },
    )
    ship_address: Optional[ShipAddress] = field(
        default=None,
        metadata={
            "name": "ShipAddress",
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
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
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
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
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
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8,
        },
    )
    contacts: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element",
        },
    )
    name_on_check: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameOnCheck",
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
    additional_notes_ret: List[AdditionalNotesRet] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesRet",
            "type": "Element",
        },
    )
    vendor_type_ref: Optional[VendorTypeRef] = field(
        default=None,
        metadata={
            "name": "VendorTypeRef",
            "type": "Element",
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    vendor_tax_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "VendorTaxIdent",
            "type": "Element",
            "max_length": 15,
        },
    )
    is_vendor_eligible_for1099: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVendorEligibleFor1099",
            "type": "Element",
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Balance",
            "type": "Element",
        },
    )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
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
    prefill_account_ref: List[PrefillAccountRef] = field(
        default_factory=list,
        metadata={
            "name": "PrefillAccountRef",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
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


class Vendors(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Vendor"
        plural_of = Vendor
