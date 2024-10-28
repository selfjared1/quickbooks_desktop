from dataclasses import dataclass, field

from typing import Optional, List, Type
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin,
)
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import ParentRef, NameFilter, NameRangeFilter



@dataclass
class PaymentMethodRef(QBRefMixin):

    class Meta:
        name = "PaymentMethodRef"

@dataclass
class PaymentMethodQuery(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "PaymentMethodType", "IncludeRetElement"
    ]

    class Meta:
        name = "PaymentMethodQuery"

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
    payment_method_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
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
class PaymentMethodAdd:
    FIELD_ORDER = [
        "Name", "IsActive", "PaymentMethodType"
    ]

    class Meta:
        name = "PaymentMethodQuery"

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
    payment_method_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
        },
    )
    
@dataclass
class PaymentMethod(QBMixinWithQuery):
    
    class Meta:
        name = "PaymentMethod"

    Query: Type[PaymentMethodQuery] = PaymentMethodQuery
    Add: Type[PaymentMethodAdd] = PaymentMethodAdd
    # There is no Mod
    
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
    payment_method_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentMethodType",
            "type": "Element",
            "valid_values": [
                "AmericanExpress", "Cash", "Check", "DebitCard", "Discover",
                "ECheck", "GiftCard", "MasterCard", "Other", "OtherCreditCard", "Visa"
            ],
        },
    )
    
class PaymentMethods(PluralMixin):

    class Meta:
        name = "PaymentMethod"
        plural_of = PaymentMethod