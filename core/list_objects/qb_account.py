from core.base import QBListBase
from core.special_fields import QBDates

class QBAccount_Query:
    def __init__(self):
        self.ListIDList = []
        self.FullNameList = []
        self.MaxReturned = None
        self.ActiveStatus = None  # e.g., "Active", "Inactive", "All"
        self.FromModifiedDate = QBDates('')
        self.ToModifiedDate = QBDates('')
        self.IncludeRetElement = []


class QBAccount(QBListBase):
    qb_object_name = 'Account'
    validated_attributes = {
        'EditSequence': 16,
        'Name': 31,
        'FullName': 159,
        'AccountNumber': 7,
        'BankNumber': 25,
        'Desc': 200
    }

    def __init__(self):
        super().__init__()
        self.TimeCreated = None
        self.TimeModified = None
        self.IsActive = None
        self.ParentRefListID = None
        self.ParentRefFullName = None
        self.Sublevel = None
        self.AccountType = None
        self.SpecialAccountType = None
        self.Balance = None
        self.TotalBalance = None
        self.TaxLineID = None
        self.TaxLineName = None
        self.CashFlowClassification = None
        self.CurrencyRefListID = None
        self.CurrencyRefFullName = None

        for attribute, max_len in self.validated_attributes.items():
            self.add_validated_property(attribute, max_len)