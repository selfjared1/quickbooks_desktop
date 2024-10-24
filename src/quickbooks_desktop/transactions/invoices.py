from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralMixin, PluralListSaveMixin
from src.quickbooks_desktop.common_and_special_fields.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin, ListSaveMixin
from src.quickbooks_desktop.common_and_special_fields.qb_other_common_fields import ParentRef
from src.quickbooks_desktop.common_and_special_fields.qb_query_common_fields import NameFilter, NameRangeFilter, CurrencyFilter
from src.quickbooks_desktop.lists.sales_tax_codes import SalesTaxCodeRef
from src.quickbooks_desktop.lists.customers import CustomerRef
from src.quickbooks_desktop.lists.qb_classes import QBClassRef
from src.quickbooks_desktop.lists.accounts import AraccountRef
from src.quickbooks_desktop.lists.currency import CurrencyRef


@dataclass
class InvoiceRet:
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
    customer_ref: Optional[CustomerRef] = field(
        default=None,
        metadata={
            "name": "CustomerRef",
            "type": "Element",
        },
    )
    class_ref: Optional[QBClassRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    araccount_ref: Optional[AraccountRef] = field(
        default=None,
        metadata={
            "name": "ARAccountRef",
            "type": "Element",
        },
    )
    template_ref: Optional[TemplateRef] = field(
        default=None,
        metadata={
            "name": "TemplateRef",
            "type": "Element",
        },
    )
    txn_date: Optional[TxnDate] = field(
        default=None,
        metadata={
            "name": "TxnDate",
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
    is_pending: Optional[IsPending] = field(
        default=None,
        metadata={
            "name": "IsPending",
            "type": "Element",
        },
    )
    is_finance_charge: Optional[IsFinanceCharge] = field(
        default=None,
        metadata={
            "name": "IsFinanceCharge",
            "type": "Element",
        },
    )
    ponumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "PONumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    terms_ref: Optional[TermsRef] = field(
        default=None,
        metadata={
            "name": "TermsRef",
            "type": "Element",
        },
    )
    due_date: Optional[DueDate] = field(
        default=None,
        metadata={
            "name": "DueDate",
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
    fob: Optional[str] = field(
        default=None,
        metadata={
            "name": "FOB",
            "type": "Element",
            "max_length": 13,
        },
    )
    ship_date: Optional[ShipDate] = field(
        default=None,
        metadata={
            "name": "ShipDate",
            "type": "Element",
        },
    )
    ship_method_ref: Optional[ShipMethodRef] = field(
        default=None,
        metadata={
            "name": "ShipMethodRef",
            "type": "Element",
        },
    )
    subtotal: Optional[Subtotal] = field(
        default=None,
        metadata={
            "name": "Subtotal",
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
    sales_tax_percentage: Optional[SalesTaxPercentage] = field(
        default=None,
        metadata={
            "name": "SalesTaxPercentage",
            "type": "Element",
        },
    )
    sales_tax_total: Optional[SalesTaxTotal] = field(
        default=None,
        metadata={
            "name": "SalesTaxTotal",
            "type": "Element",
        },
    )
    applied_amount: Optional[AppliedAmount] = field(
        default=None,
        metadata={
            "name": "AppliedAmount",
            "type": "Element",
        },
    )
    balance_remaining: Optional[BalanceRemaining] = field(
        default=None,
        metadata={
            "name": "BalanceRemaining",
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
    exchange_rate: Optional[ExchangeRate] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
        },
    )
    balance_remaining_in_home_currency: Optional[
        BalanceRemainingInHomeCurrency
    ] = field(
        default=None,
        metadata={
            "name": "BalanceRemainingInHomeCurrency",
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
    is_paid: Optional[IsPaid] = field(
        default=None,
        metadata={
            "name": "IsPaid",
            "type": "Element",
        },
    )
    customer_msg_ref: Optional[CustomerMsgRef] = field(
        default=None,
        metadata={
            "name": "CustomerMsgRef",
            "type": "Element",
        },
    )
    is_to_be_printed: Optional[IsToBePrinted] = field(
        default=None,
        metadata={
            "name": "IsToBePrinted",
            "type": "Element",
        },
    )
    is_to_be_emailed: Optional[IsToBeEmailed] = field(
        default=None,
        metadata={
            "name": "IsToBeEmailed",
            "type": "Element",
        },
    )
    is_tax_included: Optional[IsTaxIncluded] = field(
        default=None,
        metadata={
            "name": "IsTaxIncluded",
            "type": "Element",
        },
    )
    customer_sales_tax_code_ref: Optional[CustomerSalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "CustomerSalesTaxCodeRef",
            "type": "Element",
        },
    )
    suggested_discount_amount: Optional[SuggestedDiscountAmount] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountAmount",
            "type": "Element",
        },
    )
    suggested_discount_date: Optional[SuggestedDiscountDate] = field(
        default=None,
        metadata={
            "name": "SuggestedDiscountDate",
            "type": "Element",
        },
    )
    other: Optional[str] = field(
        default=None,
        metadata={
            "name": "Other",
            "type": "Element",
            "max_length": 29,
        },
    )
    external_guid: Optional[ExternalGuid] = field(
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
    invoice_line_ret: List[InvoiceLineRet] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineRet",
            "type": "Element",
        },
    )
    invoice_line_group_ret: List[InvoiceLineGroupRet] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceLineGroupRet",
            "type": "Element",
        },
    )
    discount_line_ret: Optional[DiscountLineRet] = field(
        default=None,
        metadata={
            "name": "DiscountLineRet",
            "type": "Element",
        },
    )
    sales_tax_line_ret: Optional[SalesTaxLineRet] = field(
        default=None,
        metadata={
            "name": "SalesTaxLineRet",
            "type": "Element",
        },
    )
    shipping_line_ret: Optional[ShippingLineRet] = field(
        default=None,
        metadata={
            "name": "ShippingLineRet",
            "type": "Element",
        },
    )
    data_ext_ret: List[DataExtRet] = field(
        default_factory=list,
        metadata={
            "name": "DataExtRet",
            "type": "Element",
        },
    )