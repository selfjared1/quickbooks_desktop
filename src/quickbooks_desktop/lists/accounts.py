from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type
from src.quickbooks_desktop.qb_mixin import PluralMixin
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.qb_mixin import QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin, ListSaveMixin, PluralListSaveMixin
from src.quickbooks_desktop.qb_other_common_fields import ParentRef
from src.quickbooks_desktop.qb_query_common_fields import NameFilter, NameRangeFilter, CurrencyFilter
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


@dataclass
class AccountRef(QBRefMixin):

    class Meta:
        name = "AccountRef"


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
class AccountQuery(QBQueryMixin):

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
    account_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AccountType",
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
    # meta_data: AccountQueryRqTypeMetaData = field(
    #     default=AccountQueryRqTypeMetaData.NO_META_DATA,
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )

    VALID_ACCOUNT_TYPE_VALUES = VALID_ACCOUNT_TYPE_VALUES

    def __post_init__(self):
        for single_account_type in self.account_type:
            self._validate_str_from_list_of_values('account_type', single_account_type, self.VALID_ACCOUNT_TYPE_VALUES)


@dataclass
class AccountAdd(QBAddMixin):

    class Meta:
        name = "AccountAdd"

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
            "required": True,
        },
    )
    detail_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailAccountType",
            "type": "Element",
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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
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

    VALID_ACCOUNT_TYPE_VALUES = VALID_ACCOUNT_TYPE_VALUES
    VALID_DETAIL_ACCOUNT_TYPE_VALUES = VALID_DETAIL_ACCOUNT_TYPE_VALUES

    def __post_init__(self):
        self._validate_str_from_list_of_values('wage_type', self.account_type, self.VALID_ACCOUNT_TYPE_VALUES)
        self._validate_str_from_list_of_values('detail_account_type', self.detail_account_type, self.VALID_DETAIL_ACCOUNT_TYPE_VALUES)


@dataclass
class AccountMod(QBModMixin):

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
    sales_tax_code_ref: Optional[SalesTaxCodeRef] = field(
        default=None,
        metadata={
            "name": "SalesTaxCodeRef",
            "type": "Element",
        },
    )
    tax_line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxLineID",
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

    VALID_ACCOUNT_TYPE_VALUES = VALID_ACCOUNT_TYPE_VALUES

    def __post_init__(self):
        self._validate_str_from_list_of_values('wage_type', self.account_type, self.VALID_ACCOUNT_TYPE_VALUES)


@dataclass
class Account(QBMixinWithQuery, ListSaveMixin):

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
    sublevel: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sublevel",
            "type": "Element",
        },
    )
    account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountType",
            "type": "Element",
        },
    )
    detail_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailAccountType",
            "type": "Element",
        },
    )
    special_account_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialAccountType",
            "type": "Element",
        },
    )
    is_tax_account: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsTaxAccount",
            "type": "Element",
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
    last_check_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastCheckNumber",
            "type": "Element",
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
        },
    )

    #todo: Add Field
    # currency_ref: Optional[CurrencyRef] = field(
    #     default=None,
    #     metadata={
    #         "name": "CurrencyRef",
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

    VALID_ACCOUNT_TYPE_VALUES = VALID_ACCOUNT_TYPE_VALUES
    VALID_DETAIL_ACCOUNT_TYPE_VALUES = VALID_DETAIL_ACCOUNT_TYPE_VALUES
    VALID_SPECIAL_ACCOUNT_TYPE_VALUES = VALID_SPECIAL_ACCOUNT_TYPE_VALUES
    VALID_CASH_FLOW_CLASSIFICATION_VALUES = ["None", "Operating", "Investing", "Financing", "NotApplicable"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('wage_type', self.account_type, self.VALID_ACCOUNT_TYPE_VALUES)
        self._validate_str_from_list_of_values('detail_account_type', self.detail_account_type, self.VALID_DETAIL_ACCOUNT_TYPE_VALUES)
        self._validate_str_from_list_of_values('special_account_type', self.special_account_type, self.VALID_SPECIAL_ACCOUNT_TYPE_VALUES)
        self._validate_str_from_list_of_values('cash_flow_classification', self.cash_flow_classification, self.VALID_CASH_FLOW_CLASSIFICATION_VALUES)

class Accounts(PluralMixin):

    class Meta:
        name = "Account"
        plural_of = Account
        #todo: plural_of_db_model = DBAccount