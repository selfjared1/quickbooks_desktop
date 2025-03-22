from dataclasses import dataclass, field, fields, is_dataclass, MISSING
from typing import Optional, Union, Dict, Type, Any, get_origin, get_args, List, TypeVar
from decimal import Decimal, ROUND_HALF_UP
import re


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

VALID_REPORT_TXN_TYPE_VALUES = ["All"] + VALID_TXN_TYPE_VALUES

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

VALID_REPORT_ACCOUNT_TYPE_VALUES = [
    "AccountsPayable", "AccountsReceivable", "AllowedFor1099", "APAndSalesTax", "APOrCreditCard", "ARAndAP",
    "Asset", "BalanceSheet", "Bank", "BankAndARAndAPAndUF", "BankAndUF", "CostOfSales", "CreditCard",
    "CurrentAsset", "CurrentAssetAndExpense", "CurrentLiability", "Equity", "EquityAndIncomeAndExpense",
    "ExpenseAndOtherExpense", "FixedAsset", "IncomeAndExpense", "IncomeAndOtherIncome", "Liability",
    "LiabilityAndEquity", "LongTermLiability", "NonPosting", "OrdinaryExpense", "OrdinaryIncome",
    "OrdinaryIncomeAndCOGS", "OrdinaryIncomeAndExpense", "OtherAsset", "OtherCurrentAsset",
    "OtherCurrentLiability", "OtherExpense", "OtherIncome", "OtherIncomeOrExpense"
]

VALID_REPORT_ITEM_TYPE = [
    "AllExceptFixedAsset", "Assembly", "Discount", "FixedAsset", "Inventory",
    "InventoryAndAssembly", "NonInventory", "OtherCharge", "Payment", "Sales",
    "SalesTax", "Service"
]

VALID_SUMMARIZE_ROWS_BY = [
    "Account", "BalanceSheet", "Class", "Customer", "CustomerType", "Day", "Employee",
    "FourWeek", "HalfMonth", "IncomeStatement", "ItemDetail", "ItemType", "Month",
    "Payee", "PaymentMethod", "PayrollItemDetail", "PayrollYtdDetail", "Quarter",
    "SalesRep", "SalesTaxCode", "ShipMethod", "TaxLine", "Terms", "TotalOnly",
    "TwoWeek", "Vendor", "VendorType", "Week", "Year"
]

VALID_SUMMARIZE_COLUMNS_BY = [
    "Account", "BalanceSheet", "Class", "Customer", "CustomerType", "Day", "Employee",
    "FourWeek", "HalfMonth", "IncomeStatement", "ItemDetail", "ItemType", "Month", "Payee",
    "PaymentMethod", "PayrollItemDetail", "PayrollYtdDetail", "Quarter", "SalesRep",
    "SalesTaxCode", "ShipMethod", "Terms", "TotalOnly", "TwoWeek", "Vendor",
    "VendorType", "Week", "Year"
]

VALID_INCLUDE_COLUMN_VALUES = [
    "Account", "Aging", "Amount", "AmountDifference", "AverageCost", "BilledDate",
    "BillingStatus", "CalculatedAmount", "Class", "ClearedStatus", "CostPrice", "Credit",
    "Currency", "Date", "Debit", "DeliveryDate", "DueDate", "EstimateActive", "ExchangeRate",
    "FOB", "IncomeSubjectToTax", "Invoiced", "Item", "ItemDesc", "LastModifiedBy",
    "LatestOrPriorState", "Memo", "ModifiedTime", "Name", "NameAccountNumber", "NameAddress",
    "NameCity", "NameContact", "NameEmail", "NameFax", "NamePhone", "NameState", "NameZip",
    "OpenBalance", "OriginalAmount", "PaidAmount", "PaidStatus", "PaidThroughDate",
    "PaymentMethod", "PayrollItem", "PONumber", "PrintStatus", "ProgressAmount",
    "ProgressPercent", "Quantity", "QuantityAvailable", "QuantityOnHand", "QuantityOnSalesOrder",
    "ReceivedQuantity", "RefNumber", "RunningBalance", "SalesRep", "SalesTaxCode",
    "SerialOrLotNumber", "ShipDate", "ShipMethod", "SourceName", "SplitAccount",
    "SSNOrTaxID", "TaxLine", "TaxTableVersion", "Terms", "TxnID", "TxnNumber",
    "TxnType", "UnitPrice", "UserEdit", "ValueOnHand", "WageBase", "WageBaseTips"
]

VALID_REPORT_DETAIL_LEVEL_FILTERS = ["All", "AllExceptSummary", "SummaryOnly"]

VALID_REPORT_POSTING_STATUS_FILTER = ["Either", "NonPosting", "Posting"]

VALID_RETURN_ROWS = ["ActiveOnly", "NonZero", "All"]

VALID_REPORT_CALENDAR = ["CalendarYear", "FiscalYear", "TaxYear"]

VALID_RETURN_COLUMNS = ["ActiveOnly", "NonZero", "All"]

VALID_REPORT_BASIS = ["Accrual", "Cash", "None"]

VALID_COL_TYPE_VALUES = [
    "Account", "Addr1", "Addr2", "Addr3", "Addr4", "Addr5", "Aging", "Amount",
    "AmountDifference", "AverageCost", "BilledDate", "BillingStatus", "Blank",
    "CalculatedAmount", "Class", "ClearedStatus", "CostPrice", "CreateDate", "Credit",
    "CustomField", "Date", "Debit", "DeliveryDate", "DueDate", "Duration",
    "EarliestReceiptDate", "EstimateActive", "FOB", "IncomeSubjectToTax", "Invoiced",
    "IsAdjustment", "Item", "ItemDesc", "ItemVendor", "Label", "LastModifiedBy",
    "LatestOrPriorState", "Memo", "ModifiedTime", "Name", "NameAccountNumber",
    "NameAddress", "NameCity", "NameContact", "NameEmail", "NameFax", "NamePhone",
    "NameState", "NameZip", "OpenBalance", "OriginalAmount", "PaidAmount",
    "PaidStatus", "PaidThroughDate", "PaymentMethod", "PayrollItem", "Percent",
    "PercentChange", "PercentOfTotalRetail", "PercentOfTotalValue", "PhysicalCount",
    "PONumber", "PrintStatus", "ProgressAmount", "ProgressPercent", "Quantity",
    "QuantityAvailable", "QuantityOnHand", "QuantityOnOrder", "QuantityOnPendingBuild",
    "QuantityOnSalesOrder", "ReceivedQuantity", "RefNumber", "ReorderPoint",
    "RetailValueOnHand", "RunningBalance", "SalesPerWeek", "SalesRep", "SalesTaxCode",
    "ShipDate", "ShipMethod", "ShipToAddr1", "ShipToAddr2", "ShipToAddr3",
    "ShipToAddr4", "ShipToAddr5", "SONumber", "SourceName", "SplitAccount",
    "SSNOrTaxID", "SuggestedReorder", "TaxLine", "TaxTableVersion", "Terms", "Total",
    "TxnID", "TxnNumber", "TxnType", "UnitPrice", "UserEdit", "ValueOnHand",
    "WageBase", "WageBaseTips"
]

VALID_ROW_DATA_ROW_TYPE_VALUES = [
    "account", "class", "customer", "customerMessage", "customerType", "employee",
    "item", "jobType", "label", "memorizedTxn", "memorizedReport", "name",
    "otherName", "paymentMethod", "payrollItem", "salesRep", "salesTaxCode",
    "shipMethod", "state", "style", "terms", "toDo", "vendor", "vendorType"
]

VALID_COL_DATA_DATA_TYPE_VALUES = [
    "IDTYPE", "GUIDTYPE", "STRTYPE", "BOOLTYPE", "DATETYPE", "DATETIMETYPE",
    "TIMEINTERVALTYPE", "AMTTYPE", "PRICETYPE", "QUANTYPE", "PERCENTTYPE",
    "ENUMTYPE", "INTTYPE"
]

VALID_GENERAL_SUMMARY_REPORT_TYPE_VALUES = [
    "BalanceSheetByClass", "BalanceSheetPrevYearComp", "BalanceSheetStandard", "BalanceSheetSummary",
    "CustomerBalanceSummary", "ExpenseByVendorSummary", "IncomeByCustomerSummary", "InventoryStockStatusByItem",
    "InventoryStockStatusByVendor", "IncomeTaxSummary", "InventoryValuationSummary", "InventoryValuationSummaryBySite",
    "LotNumberInStockBySite", "PhysicalInventoryWorksheet", "ProfitAndLossByClass", "ProfitAndLossByJob",
    "ProfitAndLossPrevYearComp", "ProfitAndLossStandard", "ProfitAndLossYTDComp", "PurchaseByItemSummary",
    "PurchaseByVendorSummary", "SalesByCustomerSummary", "SalesByItemSummary", "SalesByRepSummary",
    "SalesTaxLiability", "SalesTaxRevenueSummary", "SerialNumberInStockBySite", "TrialBalance",
    "VendorBalanceSummary"
]

VALID_GENERAL_DETAIL_REPORT_TYPE_VALUES = [
    "1099Detail", "AuditTrail", "BalanceSheetDetail", "CheckDetail", "CustomerBalanceDetail",
    "DepositDetail", "EstimatesByJob", "ExpenseByVendorDetail", "GeneralLedger",
    "IncomeByCustomerDetail", "IncomeTaxDetail", "InventoryValuationDetail",
    "JobProgressInvoicesVsEstimates", "Journal", "MissingChecks", "OpenInvoices",
    "OpenPOs", "OpenPOsByJob", "OpenSalesOrderByCustomer", "OpenSalesOrderByItem",
    "PendingSales", "ProfitAndLossDetail", "PurchaseByItemDetail", "PurchaseByVendorDetail",
    "SalesByCustomerDetail", "SalesByItemDetail", "SalesByRepDetail", "TxnDetailByAccount",
    "TxnListByCustomer", "TxnListByDate", "TxnListByVendor", "UnpaidBillsDetail",
    "UnbilledCostsByJob", "VendorBalanceDetail"
]

VALID_AGING_REPORT_TYPE_VALUES = [
    "APAgingDetail", "APAgingSummary", "ARAgingDetail", "ARAgingSummary", "CollectionsReport"
]

VALID_PAYROLL_DETAIL_REPORT_TYPE_VALUES = [
    "EmployeeStateTaxesDetail", "PayrollItemDetail", "PayrollReviewDetail",
    "PayrollTransactionDetail", "PayrollTransactionsByPayee"
]

VALID_REPORT_DATE_MACRO_VALUES = [
    "All", "Today", "ThisWeek", "ThisWeekToDate", "ThisMonth", "ThisMonthToDate",
    "ThisQuarter", "ThisQuarterToDate", "ThisYear", "ThisYearToDate", "Yesterday",
    "LastWeek", "LastWeekToDate", "LastMonth", "LastMonthToDate", "LastQuarter",
    "LastQuarterToDate", "LastYear", "LastYearToDate", "NextWeek", "NextFourWeeks",
    "NextMonth", "NextQuarter", "NextYear"
]



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




