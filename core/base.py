from core.mixins import QBDesktopObjectBaseMixin

class QBListBase(QBDesktopObjectBaseMixin):
    def __init__(self):
        super(QBListBase, self).__init__()
        self.ListID = ""
        self.IsActive = ""
        self.ParentRef = ""

class QBTransactionBase(QBDesktopObjectBaseMixin):
    """" Multi currency is not supported yet"""
    linked_txn = {}
    def __init__(self):
        super(QBTransactionBase).__init__()
        self.TxnID = ""
        self.TxnNumber = ""
        self.RefNumber = ""
        self.Memo = ""
        self.ExternalGUID = ""
        self.LinkedTxn = ""
