from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal
from src.quickbooks_desktop.lists import (
    AccountRef, IncomeAccountRef, ExpenseAccountRef, ClassInQBRef, PrefVendorRef, SalesTaxCodeRef,
    PurchaseTaxCodeRef, CogsaccountRef, AssetAccountRef, DepositToAccountRef,
    PaymentMethodRef, TaxVendorRef
)
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixinWithQuery, QBQueryMixin, QBMixin, QBAddMixin, QBModMixin
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin
from src.quickbooks_desktop.common import ParentRef, SalesTaxReturnLineRef, NameFilter, NameRangeFilter, ClassFilter
from src.quickbooks_desktop.qb_special_fields import QBDates, QBPriceType



@dataclass
class UnitOfMeasureSetRef(QBRefMixin):
    class Meta:
        name = "UnitOfMeasureSetRef"

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

    class Meta:
        name = "ItemDiscountQuery"


@dataclass
class ItemGroupQuery(ItemQueryMixin):

    class Meta:
        name = "ItemGroupQuery"


@dataclass
class ItemServiceQuery(ItemQueryMixinWithClass):

    class Meta:
        name = "ItemServiceQuery"


@dataclass
class ItemInventoryAssemblyQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemInventoryAssemblyQuery"


@dataclass
class ItemInventoryQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemInventoryQuery"


@dataclass
class ItemNonInventoryQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemNonInventoryQuery"


@dataclass
class ItemOtherChargeQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemOtherChargeQuery"


@dataclass
class ItemPaymentQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemPaymentQuery"


@dataclass
class ItemSalesTaxGroupQuery(ItemQueryMixin):

    class Meta:
        name = "ItemSalesTaxGroupQuery"


@dataclass
class ItemSalesTaxQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemSalesTaxQuery"

@dataclass
class ItemServiceQuery(ItemQueryMixinWithClass):
    class Meta:
        name = "ItemServiceQuery"


@dataclass
class ItemSubtotalQuery(ItemQueryMixin):

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
    quantity_on_hand: Optional[int] = field(
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

#******************************************************

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

#todo:  Finish comparing Mods from here.
#todo: Create the classes that hold query, add, and Mod

@dataclass
class ItemNonInventoryMod(ItemModWithClassAndTaxMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ParentRef", "ClassRef",
        "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
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
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "SalesTaxCodeRef", "SalesOrPurchase", "SalesAndPurchase", "ExternalGUID"
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
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "DepositToAccountRef", "PaymentMethodRef", "ExternalGUID"
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
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ItemDesc",
        "TaxRate", "TaxVendorRef", "ExternalGUID"
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
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID",
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
class ItemServiceMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ClassRef", "ParentRef",
        "UnitOfMeasureSetRef", "SalesTaxCodeRef", "SalesOrPurchase",
        "SalesAndPurchase", "ExternalGUID"
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


class ItemSubtotalMod(ItemModMixin):
    FIELD_ORDER = [
        "ListID", "EditSequence", "Name", "BarCode", "IsActive", "ItemDesc", "ExternalGUID"
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


#******************************************************

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


