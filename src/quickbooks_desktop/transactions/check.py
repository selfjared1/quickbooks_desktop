from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.data_ext import DataExt

from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    LinkedTxn, CurrencyFilter, PayeeEntityRef, Address, AddressBlock, ExpenseLineAdd,
    ItemLineAdd, ItemGroupLineAdd, ExpenseLineMod, ItemLineMod, ItemGroupLineMod,
    ExpenseLine, ItemLine, ItemGroupLine
)
from src.quickbooks_desktop.lists import (
    AccountRef, SalesTaxCodeRef, CurrencyRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBMixinWithQuery,
    QBQueryMixin, QBAddMixin, QBModMixin
)


@dataclass
class ApplyCheckToTxnBase:

    class Meta:
        name = ""

    txn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TxnID",
            "type": "Element",
            "required": True,
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )


@dataclass
class ApplyCheckToTxnAdd(ApplyCheckToTxnBase, QBAddMixin):

    class Meta:
        name = "ApplyCheckToTxnAdd"


@dataclass
class ApplyCheckToTxnMod(ApplyCheckToTxnBase, QBAddMixin):

    class Meta:
        name = "ApplyCheckToTxnMod"


@dataclass
class CheckQuery(QBQueryMixin):
    FIELD_ORDER = [
        "metaData", "iterator", "iteratorID", "TxnID", "RefNumber",
        "RefNumberCaseSensitive", "MaxReturned", "ModifiedDateRangeFilter",
        "TxnDateRangeFilter", "EntityFilter", "AccountFilter", "RefNumberFilter",
        "RefNumberRangeFilter", "CurrencyFilter", "IncludeLineItems",
        "IncludeLinkedTxns", "IncludeRetElement", "OwnerID"
    ]

    class Meta:
        name = "CheckQuery"

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
    entity_filter: Optional[EntityFilter] = field(
        default=None,
        metadata={
            "name": "EntityFilter",
            "type": "Element",
        },
    )
    account_filter: Optional[AccountFilter] = field(
        default=None,
        metadata={
            "name": "AccountFilter",
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
    currency_filter: Optional[CurrencyFilter] = field(
        default=None,
        metadata={
            "name": "CurrencyFilter",
            "type": "Element",
        },
    )
    include_line_items: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLineItems",
            "type": "Element",
        },
    )
    include_linked_txns: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IncludeLinkedTxns",
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
class CheckAdd(QBAddMixin):
    FIELD_ORDER = [
        "defMacro", "AccountRef", "PayeeEntityRef", "RefNumber", "TxnDate",
        "Memo", "Address", "IsToBePrinted", "ExchangeRate", "ExternalGUID",
        "ApplyCheckToTxnAdd", "ExpenseLineAdd", "ItemLineAdd", "ItemGroupLineAdd"
    ]

    class Meta:
        name = "CheckAdd"

    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
            "required": True,
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
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
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
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
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
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
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
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
    apply_check_to_txn_add: List[ApplyCheckToTxnAdd] = field(
        default_factory=list,
        metadata={
            "name": "ApplyCheckToTxnAdd",
            "type": "Element",
        },
    )
    expense_line_add: List[ExpenseLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineAdd",
            "type": "Element",
        },
    )
    item_line_add: List[ItemLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineAdd",
            "type": "Element",
        },
    )
    item_group_line_add: List[ItemGroupLineAdd] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineAdd",
            "type": "Element",
        },
    )
    def_macro: Optional[str] = field(
        default=None,
        metadata={
            "name": "defMacro",
            "type": "Attribute",
        },
    )


@dataclass
class CheckMod(QBModMixin):
    FIELD_ORDER = [
        "TxnID", "EditSequence", "AccountRef", "PayeeEntityRef", "RefNumber",
        "TxnDate", "Memo", "Address", "IsToBePrinted", "ExchangeRate",
        "ApplyCheckToTxnMod", "ClearExpenseLines", "ExpenseLineMod",
        "ClearItemLines", "ItemLineMod", "ItemGroupLineMod"
    ]

    class Meta:
        name = "CheckMod"

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
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
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
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
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
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
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
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    apply_check_to_txn_mod: List[ApplyCheckToTxnMod] = field(
        default_factory=list,
        metadata={
            "name": "ApplyCheckToTxnMod",
            "type": "Element",
        },
    )
    clear_expense_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearExpenseLines",
            "type": "Element",
        },
    )
    expense_line_mod: List[ExpenseLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineMod",
            "type": "Element",
        },
    )
    clear_item_lines: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearItemLines",
            "type": "Element",
        },
    )
    item_line_mod: List[ItemLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineMod",
            "type": "Element",
        },
    )
    item_group_line_mod: List[ItemGroupLineMod] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineMod",
            "type": "Element",
        },
    )
    

@dataclass
class Check(QBMixinWithQuery):
    
    class Meta:
        name = "Check"
    
    Query: Type[CheckQuery] = CheckQuery
    Add: Type[CheckAdd] = CheckAdd
    Mod: Type[CheckMod] = CheckMod
    
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
    account_ref: Optional[AccountRef] = field(
        default=None,
        metadata={
            "name": "AccountRef",
            "type": "Element",
        },
    )
    payee_entity_ref: Optional[PayeeEntityRef] = field(
        default=None,
        metadata={
            "name": "PayeeEntityRef",
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
    txn_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TxnDate",
            "type": "Element",
        },
    )
    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )
    exchange_rate: Optional[float] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    amount_in_home_currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AmountInHomeCurrency",
            "type": "Element",
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
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
        },
    )
    address_block: Optional[AddressBlock] = field(
        default=None,
        metadata={
            "name": "AddressBlock",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
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
    linked_txn: List[LinkedTxn] = field(
        default_factory=list,
        metadata={
            "name": "LinkedTxn",
            "type": "Element",
        },
    )
    expense_line_ret: List[ExpenseLine] = field(
        default_factory=list,
        metadata={
            "name": "ExpenseLineRet",
            "type": "Element",
        },
    )
    item_line_ret: List[ItemLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemLineRet",
            "type": "Element",
        },
    )
    item_group_line_ret: List[ItemGroupLine] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroupLineRet",
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


class Checks(PluralMixin, PluralTrxnSaveMixin):

    class Meta:
        name = "Check"
        plural_of = Check