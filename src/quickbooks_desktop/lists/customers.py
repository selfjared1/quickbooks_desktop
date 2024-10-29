from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.mixins.qb_mixins import (
    QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBAddMixin, QBModMixin, QBMixin
)
from src.quickbooks_desktop.lists import (
    ClassInQBRef, SalesRepRef, TermsRef, SalesTaxCodeRef, ItemSalesTaxRef, PriceLevelRef, CurrencyRef,
)

from src.quickbooks_desktop.common import (
    ParentRef, NameFilter, NameRangeFilter, TotalBalanceFilter, CurrencyFilter, Contacts,
    ClassFilter, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, ShipToAddress,
    AdditionalContactRef, PreferredPaymentMethodRef, CreditCardInfo, JobTypeRef, AdditionalNotes,
    ContactsMod, AdditionalNotesMod, AdditionalNotesRet
)



@dataclass
class CustomerRef(QBRefMixin):
    class Meta:
        name = "CustomerRef"

@dataclass
class CustomerTypeRef(QBRefMixin):
    class Meta:
        name = "CustomerTypeRef"


@dataclass
class CustomerQuery(QBQueryMixin):

    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "total_balance_filter", "currency_filter",
        "class_filter", "include_ret_element", "owner_id"
    ]

    class Meta:
        name = "CustomerQuery"

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
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    #todo: Add Field
    # meta_data: CustomerQueryRqTypeMetaData = field(
    #     default=CustomerQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )
    # iterator: Optional[CustomerQueryRqTypeIterator] = field(
    #     default=None,
    #     metadata={
    #         "type": "Attribute",
    #     },
    # )
    # iterator_id: Optional[str] = field(
    #     default=None,
    #     metadata={
    #         "name": "iteratorID",
    #         "type": "Attribute",
    #     },
    # )

@dataclass
class CustomerAdd(QBAddMixin):
    FIELD_ORDER = [
        "Name", "IsActive", "ClassRef", "ParentRef", "CompanyName", "Salutation",
        "FirstName", "MiddleName", "LastName", "JobTitle", "BillAddress",
        "ShipAddress", "ShipToAddress", "Phone", "AltPhone", "Fax", "Email", "Cc",
        "Contact", "AltContact", "AdditionalContactRef", "Contacts",
        "CustomerTypeRef", "TermsRef", "SalesRepRef", "OpenBalance",
        "OpenBalanceDate", "SalesTaxCodeRef", "ItemSalesTaxRef", "ResaleNumber",
        "AccountNumber", "CreditLimit", "PreferredPaymentMethodRef",
        "CreditCardInfo", "JobStatus", "JobStartDate", "JobProjectedEndDate",
        "JobEndDate", "JobDesc", "JobTypeRef", "Notes", "AdditionalNotes",
        "PreferredDeliveryMethod", "PriceLevelRef", "ExternalGUID", "CurrencyRef"
    ]

    class Meta:
        name = "CustomerAdd"

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
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
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
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
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
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
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
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    sales_tax_country: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesTaxCountry",
            "type": "Element",
            "valid_values": ["Australia", "Canada", "UK", "US"]
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15,
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
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element",
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element",
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element",
            "valid_values": ["Awarded", "Closed", "InProgress", "None", "NotAwarded", "Pending"]
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element",
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element",
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element",
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99,
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element",
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
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
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
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30,
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
class CustomerMod(QBModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "IsActive", "ClassRef", "ParentRef",
        "CompanyName", "Salutation", "FirstName", "MiddleName", "LastName",
        "JobTitle", "BillAddress", "ShipAddress", "ShipToAddress", "Phone",
        "AltPhone", "Fax", "Email", "Cc", "Contact", "AltContact",
        "AdditionalContactRef", "ContactsMod", "CustomerTypeRef", "TermsRef",
        "SalesRepRef", "SalesTaxCodeRef", "ItemSalesTaxRef", "ResaleNumber",
        "AccountNumber", "CreditLimit", "PreferredPaymentMethodRef",
        "CreditCardInfo", "JobStatus", "JobStartDate", "JobProjectedEndDate",
        "JobEndDate", "JobDesc", "JobTypeRef", "Notes", "AdditionalNotesMod",
        "PreferredDeliveryMethod", "PriceLevelRef", "CurrencyRef"
    ]

    class Meta:
        name = "CustomerMod"

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
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
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
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
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
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
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
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element",
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15,
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
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element",
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element",
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element",
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element",
            "valid_values": ["Awarded", "Closed", "InProgress", "None", "NotAwarded", "Pending"]
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element",
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element",
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element",
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99,
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element",
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
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element",
        },
    )
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30,
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
class Customer(QBMixinWithQuery):
    class Meta:
        name = "Customer"

    Query: Type[CustomerQuery] = CustomerQuery
    Add: Type[CustomerAdd] = CustomerAdd
    Mod: Type[CustomerMod] = CustomerMod

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
            "type": "Element"
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element"
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41
        },
    )
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 209
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element"
        },
    )
    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element"
        },
    )
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element"
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element"
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
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
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element"
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
    bill_address: Optional[BillAddress] = field(
        default=None,
        metadata={
            "name": "BillAddress",
            "type": "Element",
        },
    )
    bill_address_block: Optional[BillAddressBlock] = field(
        default=None,
        metadata={
            "name": "BillAddressBlock",
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
    ship_address_block: Optional[ShipAddressBlock] = field(
        default=None,
        metadata={
            "name": "ShipAddressBlock",
            "type": "Element",
        },
    )
    ship_to_address: List[ShipToAddress] = field(
        default_factory=list,
        metadata={
            "name": "ShipToAddress",
            "type": "Element",
            "max_occurs": 50,
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc",
            "type": "Element",
            "max_length": 1023
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
    alt_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltContact",
            "type": "Element",
            "max_length": 41
        },
    )
    additional_contact_ref: List[AdditionalContactRef] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalContactRef",
            "type": "Element",
            "max_occurs": 8
        },
    )
    contacts_ret: List[Contacts] = field(
        default_factory=list,
        metadata={
            "name": "Contacts",
            "type": "Element"
        },
    )
    customer_type_ref: Optional[CustomerTypeRef] = field(
        default=None,
        metadata={
            "name": "CustomerTypeRef",
            "type": "Element"
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element"
        },
    )
    sales_rep_ref: Optional[SalesRepRef] = field(
        default=None,
        metadata={
            "name": "SalesRepRef",
            "type": "Element"
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Balance",
            "type": "Element"
        },
    )
    total_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalBalance",
            "type": "Element"
        },
    )
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element"
        },
    )
    item_sales_tax_ref: Optional[ItemSalesTaxRef] = field(
        default=None,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element"
        },
    )
    sales_tax_country: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesTaxCountry",
            "type": "Element",
            "valid_values": ["Australia", "Canada", "UK", "US"]
        },
    )
    resale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResaleNumber",
            "type": "Element",
            "max_length": 15
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99
        },
    )
    credit_limit: Optional[str] = field(
        default=None,
        metadata={
            "name": "CreditLimit",
            "type": "Element"
        },
    )
    preferred_payment_method_ref: Optional[PreferredPaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PreferredPaymentMethodRef",
            "type": "Element"
        },
    )
    credit_card_info: Optional[CreditCardInfo] = field(
        default=None,
        metadata={
            "name": "CreditCardInfo",
            "type": "Element"
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element"
        },
    )
    job_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobStartDate",
            "type": "Element"
        },
    )
    job_projected_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobProjectedEndDate",
            "type": "Element"
        },
    )
    job_end_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "JobEndDate",
            "type": "Element"
        },
    )
    job_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobDesc",
            "type": "Element",
            "max_length": 99
        },
    )
    job_type_ref: Optional[JobTypeRef] = field(
        default=None,
        metadata={
            "name": "JobTypeRef",
            "type": "Element"
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095
        },
    )
    additional_notes_ret: List[AdditionalNotesRet] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalNotesRet",
            "type": "Element"
        },
    )
    is_statement_with_parent: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsStatementWithParent",
            "type": "Element"
        },
    )
    preferred_delivery_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreferredDeliveryMethod",
            "type": "Element",
            "valid_values": ["None", "Email", "Fax"]
        },
    )
    price_level_ref: Optional[PriceLevelRef] = field(
        default=None,
        metadata={
            "name": "PriceLevelRef",
            "type": "Element"
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element"
        },
    )
    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "max_length": 30
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element"
        },
    )
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element"
        },
    )


class Customers(PluralMixin):

    class Meta:
        name = "Customer"
        plural_of = Customer



