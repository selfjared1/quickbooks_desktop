
AccountRet = """
    <AccountRet> 
<ListID >IDTYPE</ListID> 
<TimeCreated >DATETIMETYPE</TimeCreated> 
<TimeModified >DATETIMETYPE</TimeModified> 
<EditSequence >STRTYPE</EditSequence> 
<Name >STRTYPE</Name> 
<FullName >STRTYPE</FullName> 
<IsActive >BOOLTYPE</IsActive> 
<ParentRef> 
<ListID >IDTYPE</ListID> 
<FullName >STRTYPE</FullName> 
</ParentRef>
<Sublevel >INTTYPE</Sublevel> 
<!-- AccountType may have one of the following values: AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome -->
<AccountType >ENUMTYPE</AccountType> 
<!-- SpecialAccountType may have one of the following values: AccountsPayable, AccountsReceivable, CondenseItemAdjustmentExpenses, CostOfGoodsSold, DirectDepositLiabilities, Estimates, ExchangeGainLoss, InventoryAssets, ItemReceiptAccount, OpeningBalanceEquity, PayrollExpenses, PayrollLiabilities, PettyCash, PurchaseOrders, ReconciliationDifferences, RetainedEarnings, SalesOrders, SalesTaxPayable, UncategorizedExpenses, UncategorizedIncome, UndepositedFunds -->
<SpecialAccountType >ENUMTYPE</SpecialAccountType> 
<AccountNumber >STRTYPE</AccountNumber> 
<BankNumber >STRTYPE</BankNumber> 
<Desc >STRTYPE</Desc> 
<Balance >AMTTYPE</Balance> 
<TotalBalance >AMTTYPE</TotalBalance> 
<TaxLineInfoRet> 
<TaxLineID >INTTYPE</TaxLineID> 
<TaxLineName >STRTYPE</TaxLineName> 
</TaxLineInfoRet>
<!-- CashFlowClassification may have one of the following values: None, Operating, Investing, Financing, NotApplicable -->
<CashFlowClassification >ENUMTYPE</CashFlowClassification> 
<CurrencyRef> 
<ListID >IDTYPE</ListID> 
<FullName >STRTYPE</FullName> 
</CurrencyRef>
<DataExtRet> 
<OwnerID >GUIDTYPE</OwnerID> 
<DataExtName >STRTYPE</DataExtName> 
<!-- DataExtType may have one of the following values: AMTTYPE, DATETIMETYPE, INTTYPE, PERCENTTYPE, PRICETYPE, QUANTYPE, STR1024TYPE, STR255TYPE -->
<DataExtType >ENUMTYPE</DataExtType> 
<DataExtValue >STRTYPE</DataExtValue> 
</DataExtRet>
</AccountRet>
    """

AccountRet_base = """
    <AccountRet> 
<ListID >IDTYPE</ListID> 
<TimeCreated >DATETIMETYPE</TimeCreated> 
<TimeModified >DATETIMETYPE</TimeModified> 
<EditSequence >STRTYPE</EditSequence> 
<Name >STRTYPE</Name> 
<FullName >STRTYPE</FullName> 
<IsActive >BOOLTYPE</IsActive> 
<ParentRef> 
<ListID >IDTYPE</ListID> 
<FullName >STRTYPE</FullName> 
</ParentRef>
<Sublevel >INTTYPE</Sublevel> 
<AccountType >ENUMTYPE</AccountType> 
<SpecialAccountType >ENUMTYPE</SpecialAccountType> 
<AccountNumber >STRTYPE</AccountNumber> 
<BankNumber >STRTYPE</BankNumber> 
<Desc >STRTYPE</Desc> 
<Balance >AMTTYPE</Balance> 
<TotalBalance >AMTTYPE</TotalBalance> 
<TaxLineInfoRet> 
<TaxLineID >INTTYPE</TaxLineID> 
<TaxLineName >STRTYPE</TaxLineName> 
</TaxLineInfoRet>
<CashFlowClassification >ENUMTYPE</CashFlowClassification> 
<CurrencyRef> 
<ListID >IDTYPE</ListID> 
<FullName >STRTYPE</FullName> 
</CurrencyRef>
<DataExtRet> 
<OwnerID >GUIDTYPE</OwnerID> 
<DataExtName >STRTYPE</DataExtName> 
<DataExtType >ENUMTYPE</DataExtType> 
<DataExtValue >STRTYPE</DataExtValue> 
</DataExtRet>
</AccountRet>
    """