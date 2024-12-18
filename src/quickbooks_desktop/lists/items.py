from dataclasses import dataclass, field
from typing import Optional, List, Type
from decimal import Decimal
from src.quickbooks_desktop.lists import (
    AccountRef, IncomeAccountRef, ExpenseAccountRef, ClassInQBRef, PrefVendorRef, SalesTaxCodeRef,
    PurchaseTaxCodeRef, CogsaccountRef, AssetAccountRef, DepositToAccountRef,
    PaymentMethodRef, TaxVendorRef
)
from src.quickbooks_desktop.mixins import (
    QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBMixin, QBAddMixin, QBModMixin, PluralMixin, PluralListSaveMixin
)
from src.quickbooks_desktop.common import ParentRef, SalesTaxReturnLineRef, NameFilter, NameRangeFilter, ClassFilter
from src.quickbooks_desktop.qb_special_fields import QBDates, QBPriceType
from src.quickbooks_desktop.data_ext import DataExt



@dataclass
class UnitOfMeasureSetRef(QBRefMixin):
    class Meta:
        name = "UnitOfMeasureSetRef"

@dataclass
class ItemRef(QBRefMixin):
    class Meta:
        name = "ItemRef"


@dataclass
class ItemInventoryAssemblyRef(QBRefMixin):
    class Meta:
        name = "ItemInventoryAssemblyRef"


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
class ItemInventoryRef(QBRefMixin):
    class Meta:
        name = "ItemInventoryRef"


@dataclass
class ItemGroupLine(QBMixin):

    class Meta:
        name = "ItemGroupLine"

    item_ref: Optional[ItemRef] = field(
        default=None,
        metadata={
            "name": "ItemRef",
            "type": "Element",
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    unit_of_measure: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasure",
            "type": "Element",
            "max_length": 31,
        },
    )


@dataclass
class ItemInventoryAssemblyLine(QBMixin):

    class Meta:
        name = "ItemInventoryAssemblyLine"

    item_inventory_ref: Optional[ItemInventoryRef] = field(
        default=None,
        metadata={
            "name": "ItemInventoryRef",
            "type": "Element",
            "required": True,
        },
    )
    quantity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )


@dataclass
class BarCode(QBMixin):

    class Meta:
        name = "BarCode"

    bar_code_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "BarCodeValue",
            "type": "Element",
            "max_length": 50,
        },
    )
    assign_even_if_used: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AssignEvenIfUsed",
            "type": "Element",
        },
    )
    allow_override: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AllowOverride",
            "type": "Element",
        },
    )


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
class ItemQueryMixin(QBQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter",
        "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = ""

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
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )

@dataclass
class ItemQueryMixinWithClass(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus", "FromModifiedDate",
        "ToModifiedDate", "NameFilter", "NameRangeFilter", "ClassFilter",
        "IncludeRetElement", "OwnerID"
    ]
    class Meta:
        name = ""

    class_filter: Optional[ClassFilter] = field(
        default=None,
        metadata={
            "name": "ClassFilter",
            "type": "Element",
        },
    )


@dataclass
class ItemDiscountQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemDiscountQuery"


@dataclass
class ItemGroupQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemGroupQuery"


@dataclass
class ItemInventoryAssemblyQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemInventoryAssemblyQuery"


@dataclass
class ItemInventoryQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemInventoryQuery"


@dataclass
class ItemNonInventoryQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemNonInventoryQuery"


@dataclass
class ItemOtherChargeQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemOtherChargeQuery"


@dataclass
class ItemPaymentQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemPaymentQuery"


@dataclass
class ItemSalesTaxGroupQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemSalesTaxGroupQuery"


@dataclass
class ItemSalesTaxQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemSalesTaxQuery"

@dataclass
class ItemServiceQuery(ItemQueryMixinWithClass):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "ClassFilter", "IncludeRetElement",
        "OwnerID"
    ]

    class Meta:
        name = "ItemServiceQuery"


@dataclass
class ItemSubtotalQuery(ItemQueryMixin):
    FIELD_ORDER = [
        "ListID", "FullName", "MaxReturned", "ActiveStatus",
        "FromModifiedDate", "ToModifiedDate", "NameFilter",
        "NameRangeFilter", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "ItemSubtotalQuery"


@dataclass
class ItemAddMixin(QBAddMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    bar_code: Optional[BarCode] = field(
        default=None,
        metadata={
            "name": "BarCode",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
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
class ItemAddWithClassAndTaxMixin(ItemAddMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
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

@dataclass
class ItemDiscountAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef", "ItemDesc",
        "SalesTaxCodeRef", "DiscountRate", "DiscountRatePercent", "AccountRef",
        "ExternalGUID"
    ]

    class Meta:
        name = "ItemDiscountAdd"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    discount_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
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
class ItemGroupAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "UnitOfMeasureSetRef",
        "IsPrintItemsInGroup", "ExternalGUID", "ItemGroupLine"
    ]

    class Meta:
        name = "ItemDiscountAdd"


    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
            "type": "Element",
        },
    )

@dataclass
class ItemInventoryAddMixin(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = []

    class Meta:
        name = ""

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
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
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
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
    purchase_cost: Optional[Decimal] = field(
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
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
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
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )

    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    total_value: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalValue",
            "type": "Element",
        },
    )
    inventory_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "InventoryDate",
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
class ItemInventoryAdd(ItemInventoryAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "ReorderPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID"
    ]

    class Meta:
        name = "ItemInventoryAdd"

    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblyAdd(ItemInventoryAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "BuildPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID", "ItemInventoryAssemblyLine"
    ]

    class Meta:
        name = "ItemInventoryAssemblyAdd"

    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
            "type": "Element",
        },
    )


@dataclass
class ItemNonInventoryAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ParentRef", "ClassRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
    ]
    class Meta:
        name = "ItemNonInventoryAdd"


    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
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


@dataclass
class ItemOtherChargeAdd(ItemAddWithClassAndTaxMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "SalesTaxCodeRef", "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
    ]

    class Meta:
        name = "ItemOtherChargeAdd"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
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


@dataclass
class ItemPaymentAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "DepositToAccountRef", "PaymentMethodRef", "ExternalGUID"
    ]

    class Meta:
        name = "ItemPaymentAdd"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )

@dataclass
class ItemSalesTaxAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "TaxRate", "TaxVendorRef", "ExternalGUID"
    ]

    class Meta:
        name = "ItemSalesTaxAdd"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxGroupAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID",
        "ItemSalesTaxRef"
    ]

    class Meta:
        name = "ItemSalesTaxGroupAdd"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ItemServiceAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "UnitOfMeasureSetRef", "SalesTaxCodeRef", "SalesOrPurchase",
        "SalesAndPurchase", "ExternalGUID"
    ]

    class Meta:
        name = "ItemServiceAdd"

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

@dataclass
class ItemSubtotalAdd(ItemAddMixin):
    FIELD_ORDER = [
        "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID"
    ]

    class Meta:
        name = "ItemSubtotalAdd"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )

@dataclass
class ItemModMixin(QBModMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

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
            "required": True,
            "max_length": 31,
        },
    )
    bar_code: Optional[BarCode] = field(
        default=None,
        metadata={
            "name": "BarCode",
            "type": "Element",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )

@dataclass
class ItemModWithClassAndTaxMixin(ItemModMixin):
    FIELD_ORDER = []
    class Meta:
        name = ""

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
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


@dataclass
class ItemDiscountMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ItemDesc", "SalesTaxCodeRef", "DiscountRate",
        "DiscountRatePercent", "AccountRef", "ApplyAccountRefToExistingTxns"
    ]

    class Meta:
        name = "ItemDiscountMod"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    discount_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
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
    apply_account_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyAccountRefToExistingTxns",
            "type": "Element",
        },
    )


@dataclass
class ItemGroupMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc",
        "UnitOfMeasureSetRef", "ForceUOMChange", "IsPrintItemsInGroup",
        "ClearItemsInGroup", "ItemGroupLine"
    ]

    class Meta:
        name = "ItemDiscountMod"


    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    clear_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemsInGroup",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
            "type": "Element",
        },
    )

@dataclass
class ItemInventoryModMixin(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = []

    class Meta:
        name = ""

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
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
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
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
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
    apply_income_account_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyIncomeAccountRefToExistingTxns",
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
    purchase_cost: Optional[Decimal] = field(
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
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
            "type": "Element",
        },
    )
    apply_cogsaccount_ref_to_existing_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ApplyCOGSAccountRefToExistingTxns",
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
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )

    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )

@dataclass
class ItemInventoryMod(ItemInventoryModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ManufacturerPartNumber", "UnitOfMeasureSetRef",
        "ForceUOMChange", "SalesTaxCodeRef", "SalesDesc", "SalesPrice",
        "IncomeAccountRef", "ApplyIncomeAccountRefToExistingTxns", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "ApplyCOGSAccountRefToExistingTxns",
        "PrefVendorRef", "AssetAccountRef", "ReorderPoint", "Max"
    ]

    class Meta:
        name = "ItemInventoryMod"

    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )


@dataclass
class ItemInventoryAssemblyMod(ItemInventoryModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "COGSAccountRef", "PrefVendorRef", "AssetAccountRef",
        "BuildPoint", "Max", "QuantityOnHand", "TotalValue", "InventoryDate",
        "ExternalGUID", "ItemInventoryAssemblyLine"
    ]

    class Meta:
        name = "ItemInventoryAssemblyMod"

    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    clear_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemsInGroup",
            "type": "Element",
        },
    )
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
            "type": "Element",
        },
    )


@dataclass
class ItemNonInventoryMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "ManufacturerPartNumber", "UnitOfMeasureSetRef",
        "ForceUOMChange", "SalesTaxCodeRef", "SalesOrPurchaseMod",
        "SalesAndPurchaseMod"
    ]
    class Meta:
        name = "ItemNonInventoryMod"


    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    force_uomchange: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ForceUOMChange",
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


@dataclass
class ItemOtherChargeMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "SalesTaxCodeRef", "SalesOrPurchaseMod",
        "SalesAndPurchaseMod"
    ]

    class Meta:
        name = "ItemOtherChargeMod"

    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
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


@dataclass
class ItemPaymentMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ItemDesc", "DepositToAccountRef", "PaymentMethodRef"
    ]

    class Meta:
        name = "ItemPaymentMod"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
            "type": "Element",
        },
    )

@dataclass
class ItemSalesTaxMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ItemDesc", "TaxRate", "TaxVendorRef"
    ]

    class Meta:
        name = "ItemSalesTaxMod"

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxGroupMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc",
        "ItemSalesTaxRef"
    ]

    class Meta:
        name = "ItemSalesTaxGroupMod"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ItemServiceMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef",
        "ParentRef", "UnitOfMeasureSetRef", "ForceUOMChange", "SalesTaxCodeRef",
        "SalesOrPurchaseMod", "SalesAndPurchaseMod"
    ]

    class Meta:
        name = "ItemServiceMod"

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

@dataclass
class ItemSubtotalMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc"
    ]

    class Meta:
        name = "ItemSubtotalMod"

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )

@dataclass
class ItemMixin:
    class Meta:
        name = ""

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

@dataclass
def ItemWithClassAndTaxMixin(ItemMixin):


    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
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

@dataclass
class ItemDiscount(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemDiscount"

    Query: Type[ItemDiscountQuery] = ItemDiscountQuery
    Add: Type[ItemDiscountAdd] = ItemDiscountAdd
    Mod: Type[ItemDiscountMod] = ItemDiscountMod

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
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    discount_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRate",
            "type": "Element",
        },
    )
    discount_rate_percent: Optional[float] = field(
        default=None,
        metadata={
            "name": "DiscountRatePercent",
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemDiscounts(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemDiscount"
        plural_of = ItemDiscount


@dataclass
class ItemGroup(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemGroup"

    Query: Type[ItemGroupQuery] = ItemGroupQuery
    Add: Type[ItemGroupAdd] = ItemGroupAdd
    Mod: Type[ItemGroupMod] = ItemGroupMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    unit_of_measure_set_ref: Optional[UnitOfMeasureSetRef] = field(
        default=None,
        metadata={
            "name": "UnitOfMeasureSetRef",
            "type": "Element",
        },
    )
    is_print_items_in_group: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPrintItemsInGroup",
            "type": "Element",
        },
    )
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
        },
    )
    external_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalGUID",
            "type": "Element",
        },
    )
    item_group_line: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLine",
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
class ItemGroups(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemGroup"
        plural_of = ItemGroup


@dataclass
class ItemInventory(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemInventory"

    Query: Type[ItemInventoryQuery] = ItemInventoryQuery
    Add: Type[ItemInventoryAdd] = ItemInventoryAdd
    Mod: Type[ItemInventoryMod] = ItemInventoryMod

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
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
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
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
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
    purchase_cost: Optional[Decimal] = field(
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
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
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
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )
    reorder_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReorderPoint",
            "type": "Element",
        },
    )
    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    average_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AverageCost",
            "type": "Element",
        },
    )
    quantity_on_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnOrder",
            "type": "Element",
        },
    )
    quantity_on_sales_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemInventories(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemInventory"
        plural_of = ItemInventory


@dataclass
class ItemInventoryAssembly(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemInventoryAssembly"

    Query: Type[ItemInventoryAssemblyQuery] = ItemInventoryAssemblyQuery
    Add: Type[ItemInventoryAssemblyAdd] = ItemInventoryAssemblyAdd
    Mod: Type[ItemInventoryAssemblyMod] = ItemInventoryAssemblyMod

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
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
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
    sales_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    sales_price: Optional[Decimal] = field(
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
    purchase_cost: Optional[Decimal] = field(
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
    cogsaccount_ref: Optional[CogsaccountRef] = field(
        default=None,
        metadata={
            "name": "COGSAccountRef",
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
    asset_account_ref: Optional[AssetAccountRef] = field(
        default=None,
        metadata={
            "name": "AssetAccountRef",
            "type": "Element",
        },
    )
    build_point: Optional[int] = field(
        default=None,
        metadata={
            "name": "BuildPoint",
            "type": "Element",
        },
    )
    max: Optional[int] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Element",
        },
    )
    quantity_on_hand: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnHand",
            "type": "Element",
        },
    )
    average_cost: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AverageCost",
            "type": "Element",
        },
    )
    quantity_on_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnOrder",
            "type": "Element",
        },
    )
    quantity_on_sales_order: Optional[float] = field(
        default=None,
        metadata={
            "name": "QuantityOnSalesOrder",
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
    item_inventory_assembly_line: List[ItemInventoryAssemblyLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemInventoryAssemblyLine",
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
class ItemInventoryAssemblies(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemInventoryAssembly"
        plural_of = ItemInventoryAssembly


@dataclass
class ItemNonInventory(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemNonInventory"

    Query: Type[ItemNonInventoryQuery] = ItemNonInventoryQuery
    Add: Type[ItemNonInventoryAdd] = ItemNonInventoryAdd
    Mod: Type[ItemNonInventoryMod] = ItemNonInventoryMod

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
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Element",
            "max_length": 31,
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


@dataclass
class ItemNonInventories(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemNonInventory"
        plural_of = ItemNonInventory


@dataclass
class ItemOtherCharge(ItemWithClassAndTaxMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemOtherCharge"

    Query: Type[ItemOtherChargeQuery] = ItemOtherChargeQuery
    Add: Type[ItemOtherChargeAdd] = ItemOtherChargeAdd
    Mod: Type[ItemOtherChargeMod] = ItemOtherChargeMod

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
    is_tax_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
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
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
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


@dataclass
class ItemOtherCharges(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemOtherCharge"
        plural_of = ItemOtherCharge


@dataclass
class ItemPayment(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemPayment"

    Query: Type[ItemPaymentQuery] = ItemPaymentQuery
    Add: Type[ItemPaymentAdd] = ItemPaymentAdd
    Mod: Type[ItemPaymentMod] = ItemPaymentMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    deposit_to_account_ref: Optional[DepositToAccountRef] = field(
        default=None,
        metadata={
            "name": "DepositToAccountRef",
            "type": "Element",
        },
    )
    payment_method_ref: Optional[PaymentMethodRef] = field(
        default=None,
        metadata={
            "name": "PaymentMethodRef",
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )

@dataclass
class ItemPayments(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemPayment"
        plural_of = ItemPayment

@dataclass
class ItemSalesTax(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSalesTax"

    Query: Type[ItemSalesTaxQuery] = ItemSalesTaxQuery
    Add: Type[ItemSalesTaxAdd] = ItemSalesTaxAdd
    Mod: Type[ItemSalesTaxMod] = ItemSalesTaxMod

    class_ref: Optional[ClassInQBRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
            "max_length": 4095,
        },
    )
    tax_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
        },
    )
    tax_vendor_ref: Optional[TaxVendorRef] = field(
        default=None,
        metadata={
            "name": "TaxVendorRef",
            "type": "Element",
        },
    )
    sales_tax_return_line_ref: Optional[SalesTaxReturnLineRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxReturnLineRef",
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
    data_ext_ret: List[DataExt] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )


@dataclass
class ItemSalesTaxes(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSalesTax"
        plural_of = ItemSalesTax


@dataclass
class ItemSalesTaxGroup(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSalesTaxGroup"

    Query: Type[ItemSalesTaxGroupQuery] = ItemSalesTaxGroupQuery
    Add: Type[ItemSalesTaxGroupAdd] = ItemSalesTaxGroupAdd
    Mod: Type[ItemSalesTaxGroupMod] = ItemSalesTaxGroupMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
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
    item_sales_tax_ref: List[ItemSalesTaxRef] = field(
        default_factory=list,
        metadata={
            "name": "ItemSalesTaxRef",
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
class ItemSalesTaxGroups(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSalesTaxGroup"
        plural_of = ItemSalesTaxGroup


@dataclass
class ItemService(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemService"

    Query: Type[ItemServiceQuery] = ItemServiceQuery
    Add: Type[ItemServiceAdd] = ItemServiceAdd
    Mod: Type[ItemServiceMod] = ItemServiceMod

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


@dataclass
class ItemServices(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemService"
        plural_of = ItemService


@dataclass
class ItemSubtotal(ItemMixin, QBMixinWithQuery):
    class Meta:
        name = "ItemSubtotal"

    Query: Type[ItemSubtotalQuery] = ItemSubtotalQuery
    Add: Type[ItemSubtotalAdd] = ItemSubtotalAdd
    Mod: Type[ItemSubtotalMod] = ItemSubtotalMod

    item_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemDesc",
            "type": "Element",
        },
    )
    special_item_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialItemType",
            "type": "Element",
            "valid_values": ["FinanceCharge", "ReimbursableExpenseGroup", "ReimbursableExpenseSubtotal"]
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

@dataclass
class ItemSubtotals(PluralMixin, PluralListSaveMixin):

    class Meta:
        name = "ItemSubtotal"
        plural_of = ItemSubtotal


