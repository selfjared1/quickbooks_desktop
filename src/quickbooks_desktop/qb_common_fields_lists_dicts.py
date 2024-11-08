from dataclasses import dataclass, field, fields, is_dataclass, MISSING
from typing import Optional, Union, Dict, Type, Any, get_origin, get_args, List, TypeVar
from decimal import Decimal


TempVar = TypeVar('T')

yes_no_dict = {'Yes': True, 'yes': True, 'No': False, 'no': False}

VALID_TXN_DATA_EXT_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard",
    "BuildAssembly", "Charge", "Check", "CreditCardCharge", "CreditCardCredit",
    "CreditMemo", "Deposit", "Estimate", "InventoryAdjustment", "Invoice",
    "ItemReceipt", "JournalEntry", "PurchaseOrder", "ReceivePayment",
    "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck", "VendorCredit"
]

VALID_LIST_DATA_EXT_TYPE_VALUES = ["Account", "Customer", "Employee", "Item", "OtherName", "Vendor"]

VALID_TXN_TYPE_VALUES = [
    "ARRefundCreditCard", "Bill", "BillPaymentCheck", "BillPaymentCreditCard", "BuildAssembly",
    "Charge", "Check", "CreditCardCharge", "CreditCardCredit", "CreditMemo", "Deposit",
    "Estimate", "InventoryAdjustment", "Invoice", "ItemReceipt", "JournalEntry",
    "LiabilityAdjustment", "Paycheck", "PayrollLiabilityCheck", "PurchaseOrder",
    "ReceivePayment", "SalesOrder", "SalesReceipt", "SalesTaxPaymentCheck",
    "Transfer", "VendorCredit", "YTDAdjustment"
]

VALID_OPERATOR_VALUES = ["LessThan", "LessThanEqual", "Equal", "GreaterThan", "GreaterThanEqual"]

VALID_RELATION_VALUES = [
        "Spouse", "Partner", "Mother", "Father", "Sister", "Brother",
        "Son", "Daughter", "Friend", "Other"
    ]

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


list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
            "required": False,
        },
    )
list_ids: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
            "required": False,
        },
    )
full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Element",
            "max_length": 209,
            "required": False,
        },
    )
full_names: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
            "required": False,
        },
    )

amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "required": False,
        },
    )




