from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralListSaveMixin, QBRefMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin, SaveMixin
)
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.common import ParentRef, NameFilter, NameRangeFilter
from src.quickbooks_desktop.lists.sales_tax_codes import SalesTaxCodeRef
from src.quickbooks_desktop.lists.currency import CurrencyRef

VALID_ACCOUNT_TYPE_VALUES = [
    "AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold", "CreditCard",
    "Equity", "Expense", "FixedAsset", "Income", "LongTermLiability", "NonPosting",
    "OtherAsset", "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense", "OtherIncome"
]

VALID_DETAIL_ACCOUNT_TYPE_VALUES = [
    "AP", "AR", "AccumulatedAdjustment", "AccumulatedAmortization", "AccumulatedAmortizationOfOtherAssets",
    "AccumulatedDepletion", "AccumulatedDepreciation", "AdvertisingOrPromotional", "AllowanceForBadDebts",
    "Amortization", "Auto", "BadDebts", "BankCharges", "Buildings", "CashOnHand", "CharitableContributions",
    "Checking", "CommonStock", "CostOfLabor", "CostOfLaborCOS", "CreditCard", "DepletableAssets",
    "Depreciation", "DevelopmentCosts", "DiscountsOrRefundsGiven", "DividendIncome", "DuesAndSubscriptions",
    "EmployeeCashAdvances", "Entertainment", "EntertainmentMeals", "EquipmentRental", "EquipmentRentalCOS",
    "FederalIncomeTaxPayable", "FurnitureAndFixtures", "Goodwill", "Insurance", "InsurancePayable",
    "IntangibleAssets", "InterestEarned", "InterestPaid", "Inventory", "InvestmentMortgageOrRealEstateLoans",
    "InvestmentOther", "InvestmentTaxExemptSecurities", "InvestmentUSGovObligations", "Land", "LeaseBuyout",
    "LeaseholdImprovements", "LegalAndProfessionalFees", "Licenses", "LineOfCredit", "LoanPayable",
    "LoansToOfficers", "LoansToOthers", "LoansToStockholders", "MachineryAndEquipment", "MoneyMarket",
    "NonProfitIncome", "NotesPayable", "OfficeOrGeneralAdministrativeExpenses", "OpeningBalanceEquity",
    "OrganizationalCosts", "OtherCostsOfServiceCOS", "OtherCurrentAssets", "OtherCurrentLiab",
    "OtherFixedAssets", "OtherInvestmentIncome", "OtherLongTermAssets", "OtherLongTermLiab", "OtherMiscExpense",
    "OtherMiscIncome", "OtherMiscServiceCost", "OtherPrimaryIncome", "OwnersEquity", "PaidInCapitalOrSurplus",
    "PartnerContributions", "PartnerDistributions", "PartnersEquity", "PayrollClearing", "PayrollExpenses",
    "PayrollTaxPayable", "PenaltiesAndSettlements", "PreferredStock", "PrepaidExpenses", "PrepaidExpensesPayable",
    "PromotionalMeals", "RentOrLeaseOfBuildings", "RentsHeldInTrust", "RentsInTrustLiab", "RepairAndMaintenance",
    "Retainage", "RetainedEarnings", "SalesOfProductIncome", "SalesTaxPayable", "Savings", "SecurityDeposits",
    "ServiceOrFeeIncome", "ShareholderNotesPayable", "ShippingFreightAndDelivery", "ShippingFreightAndDeliveryCOS",
    "StateOrLocalIncomeTaxPayable", "SuppliesAndMaterials", "SuppliesAndMaterialsCOGS", "TaxExemptInterest",
    "TaxesPaid", "Travel", "TravelMeals", "TreasuryStock", "TrustAccounts", "TrustAccountsLiab",
    "UndepositedFunds", "Utilities", "Vehicles"
]

VALID_SPECIAL_ACCOUNT_TYPE_VALUES = [
    "AccountsPayable", "AccountsReceivable", "CondenseItemAdjustmentExpenses", "CostOfGoodsSold",
    "DirectDepositLiabilities", "Estimates", "ExchangeGainLoss", "InventoryAssets", "ItemReceiptAccount",
    "OpeningBalanceEquity", "PayrollExpenses", "PayrollLiabilities", "PettyCash", "PurchaseOrders",
    "ReconciliationDifferences", "RetainedEarnings", "SalesOrders", "SalesTaxPayable", "UncategorizedExpenses",
    "UncategorizedIncome", "UndepositedFunds"
]

VALID_CASH_FLOW_CLASSIFICATION_VALUES = ["None", "Operating", "Investing", "Financing", "NotApplicable"]


@dataclass
class AccountRef(QBRefMixin):
    class Meta:
        name = "AccountRef"


@dataclass
class OverrideItemAccountRef(QBRefMixin):
    class Meta:
        name = "OverrideItemAccountRef"


@dataclass
class AraccountRef(QBRefMixin):
    class Meta:
        name = "AraccountRef"


@dataclass
class DepositToAccountRef(QBRefMixin):
    class Meta:
        name = "DepositToAccountRef"


@dataclass
class ExpenseAccountRef(QBRefMixin):
    class Meta:
        name = "ExpenseAccountRef"


@dataclass
class IncomeAccountRef(QBRefMixin):
    class Meta:
        name = "IncomeAccountRef"


@dataclass
class TaxLineInfo(QBMixin):
    class Meta:
        name = "TaxLineInfo"

    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
            "type": "Element",
            "required": True,
        },
    )
    tax_line_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineName",
            "type": "Element",
            "max_length": 256,
        },
    )


@dataclass
class AccountBase:
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
    parent_ref: Optional[ParentRef] = field(
        default=None,
        metadata={
            "name": "ParentRef",
            "type": "Element",
        },
    )
    account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountType",
            "type": "Element",
            "valid_values": VALID_ACCOUNT_TYPE_VALUES,
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 7,
        },
    )
    bank_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "BankNumber",
            "type": "Element",
            "max_length": 25,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 200,
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
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )


@dataclass
class AccountQuery(QBQueryMixin):
    FIELD_ORDER = [
        "list_id", "full_name", "max_returned", "active_status",
        "from_modified_date", "to_modified_date", "name_filter",
        "name_range_filter", "account_type", "currency_filter",
        "include_ret_element", "owner_id", "request_id"
    ]

    class Meta:
        name = "AccountQuery"

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
class AccountAdd(AccountBase, QBAddMixin):
    FIELD_ORDER = [
        "name", "is_active", "parent_ref", "account_type", "account_number",
        "bank_number", "desc", "open_balance", "open_balance_date",
        "tax_line_id", "currency_ref", "include_ret_element"
    ]

    class Meta:
        name = "AccountAdd"

    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
            "type": "Element",
        },
    )


@dataclass
class AccountMod(AccountBase, QBModMixin):
    FIELD_ORDER = [
        "list_id", "edit_sequence", "name", "is_active", "parent_ref",
        "account_type", "account_number", "bank_number", "desc",
        "open_balance", "open_balance_date", "tax_line_id",
        "currency_ref", "include_ret_element"
    ]

    class Meta:
        name = "AccountMod"

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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )


@dataclass
class Account(AccountBase, QBMixinWithQuery):
    class Meta:
        name = "Account"

    Query: Type[AccountQuery] = AccountQuery
    Add: Type[AccountAdd] = AccountAdd
    Mod: Type[AccountMod] = AccountMod

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
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 159,
        },
    )
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    detail_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailAccountType",
            "type": "Element",
            "valid_values": VALID_DETAIL_ACCOUNT_TYPE_VALUES,
        },
    )
    special_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialAccountType",
            "type": "Element",
            "valid_values": VALID_SPECIAL_ACCOUNT_TYPE_VALUES,
        },
    )
    is_tax_account: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxAccount",
            "type": "Element",
        },
    )
    last_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastCheckNumber",
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
    total_balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TotalBalance",
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
    tax_line_info_ret: List[TaxLineInfo] = field(
        default_factory=list,
        metadata={
            "name": "TaxLineInfoRet",
            "type": "Element",
        },
    )
    cash_flow_classification: Optional[str] = field(
        default=None,
        metadata={
            "name": "CashFlowClassification",
            "type": "Element",
            "valid_values": VALID_CASH_FLOW_CLASSIFICATION_VALUES,
        },
    )
    currency_ref: Optional[CurrencyRef] = field(
        default=None,
        metadata={
            "name": "CurrencyRef",
            "type": "Element",
        },
    )

    # data_ext_ret: List[DataExtRet] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExtRet",
    #         "type": "Element",
    #     },
    # )


class Accounts(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "Account"
        plural_of = Account
