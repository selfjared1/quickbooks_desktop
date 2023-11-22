from special_fields import QBDateMacro, QBDate
from lxml import etree

class ModifiedDateRangeFilter:
    def __init__(self, from_date=None, to_date=None):
        self.from_qb_date = QBDate(from_date)
        self.to_qb_date = QBDate(to_date)

    def to_xml(self):
        root = etree.Element('ModifiedDateRangeFilter')
        if self.from_qb_date:
            from_date = etree.Element('FromModifiedDate')
            from_date.text = self.from_qb_date.__str__()
            root.append(from_date)
        if self.to_qb_date:
            to_date = etree.Element('ToModifiedDate')
            to_date.text = self.to_qb_date.__str__()
            root.append(to_date)
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')

class TxnDateRangeFilter:
    def __init__(self, from_date=None, to_date=None, macro=None):
        if macro:
            self.date_macro = QBDateMacro(macro)
        else:
            self.from_qb_date = QBDate(from_date)
            self.to_qb_date = QBDate(to_date)

    def to_xml(self):
        root = etree.Element('TxnDateRangeFilter')
        if self.date_macro:
            date_macro = etree.Element('DateMacro')
            date_macro.text = self.date_macro.__str__()
            root.append(date_macro)
        else:
            if self.from_qb_date:
                from_date = etree.Element('FromTxnDate')
                from_date.text = self.from_qb_date.__str__()
                root.append(from_date)
            if self.to_qb_date:
                to_date = etree.Element('ToTxnDate')
                to_date.text = self.to_qb_date.__str__()
                root.append(to_date)
            return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')