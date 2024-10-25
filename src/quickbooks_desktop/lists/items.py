from dataclasses import dataclass, field
from typing import Optional, List

from src.quickbooks_desktop.lists.accounts import AccountRef, IncomeAccountRef, ExpenseAccountRef
from src.quickbooks_desktop.lists.classes_in_qb import ClassInQBRef
from src.quickbooks_desktop.lists.vendors import PrefVendorRef
from src.quickbooks_desktop.lists.sales_tax_codes import SalesTaxCodeRef, PurchaseTaxCodeRef
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBMixin
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin
from src.quickbooks_desktop.common.qb_other_common_fields import ParentRef
from src.quickbooks_desktop.common.qb_query_common_fields import NameFilter, NameRangeFilter, ClassFilter
from src.quickbooks_desktop.qb_special_fields import QBDates, QBPriceType



@dataclass
class UnitOfMeasureSetRef(QBRefMixin):
    class Meta:
        name = "UnitOfMeasureSetRef"


@dataclass
class SalesAndPurchase(QBMixin):

    class Meta:
        name = "SalesAndPurchase"

    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "SalesPrice",
            "type": "Element",
        },
    )
    income_account_ref: Optional[IncomeAccountRef] = field(
        default=None,
        metadata={
            "name": "IncomeAccountRef",
            "type": "Element",
        },
    )
    purchase_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "PurchaseDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    purchase_cost: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "PurchaseCost",
            "type": "Element",
        },
    )
    purchase_tax_code_ref: Optional[PurchaseTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "PurchaseTaxCodeRef",
            "type": "Element",
        },
    )
    expense_account_ref: Optional[ExpenseAccountRef] = field(
        default=None,
        metadata={
            "name": "ExpenseAccountRef",
            "type": "Element",
        },
    )
    pref_vendor_ref: Optional[PrefVendorRef] = field(
        default=None,
        metadata={
            "name": "PrefVendorRef",
            "type": "Element",
        },
    )


@dataclass
class SalesOrPurchase(QBMixin):

    class Meta:
        name = "SalesOrPurchase"

    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    price: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "Price",
            "type": "Element",
        },
    )
    price_percent: Optional[QBPriceType] = field(
        default=None,
        metadata={
            "name": "PricePercent",
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

@dataclass
class ItemRef(QBRefMixin):
    class Meta:
        name = "ItemRef"


@dataclass
class ItemGroupRef(QBRefMixin):
    class Meta:
        name = "ItemGroupRef"

@dataclass
class ItemServiceRef(QBRefMixin):
    class Meta:
        name = "ItemServiceRef"

@dataclass
class ItemSalesTaxRef(QBRefMixin):
    class Meta:
        name = "ItemSalesTaxRef"


@dataclass
class ItemQueryMixin:


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

    iterator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iterator_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "iteratorID",
            "type": "Attribute",
        },
    )



@dataclass
class ItemMixin:


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
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159,
        },
    )
    bar_code_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "BarCodeValue",
            "type": "Element",
            "max_length": 50,
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
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    sales_or_purchase: Optional[SalesOrPurchase] = field(
        default=None,
        metadata={
            "name": "SalesOrPurchase",
            "type": "Element",
        },
    )
    sales_and_purchase: Optional[SalesAndPurchase] = field(
        default=None,
        metadata={
            "name": "SalesAndPurchase",
            "type": "Element",
        },
    )

    #todo:
    # external_guid: Optional[ExternalGuid] = field(
    #     default=None,
    #     metadata={
    #         "name": "ExternalGUID",
    #         "type": "Element",
    #     },
    # )
    # data_ext_ret: List[DataExtRet] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExtRet",
    #         "type": "Element",
    #     },
    # )


@dataclass
class ItemServiceQuery(QBQueryMixin, ItemQueryMixin):
    class Meta:
        name = "ItemServiceQuery"


    meta_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaData",
            "type": "Attribute",
        },
    )

    VALID_META_DATA_VALUES = ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('meta_data', self.meta_data, self.VALID_META_DATA_VALUES)


@dataclass
class ItemService(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemService"

    class Query(ItemServiceQuery):
        pass


class ItemServices(PluralMixin):

    class Meta:
        name = "ItemService"
        plural_of = ItemService
        # plural_of_db_model = DBItemService


