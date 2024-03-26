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

class QueryBase:
    def __init__(self, query_dict):
        self.MaxReturned = query_dict.get('MaxReturned', None)
        self.ModifiedDateRangeFilter = ModifiedDateRangeFilter(**query_dict.get('ModifiedDateRangeFilter', {}))
        self.IncludeRetElements = self.get_include_ret_elements(query_dict.get('IncludeRetElements', []))

    def get_include_ret_elements(self, include_ret_elements):
        if isinstance(include_ret_elements, list):
            return include_ret_elements
        elif include_ret_elements:
            return [include_ret_elements]
        else:
            return []


class TxnQuery(QueryBase):
    def __init__(self, query_dict):
        self.TxnIDs = self.get_txn_ids(query_dict.get('TxnIDs', []))
        self.MaxReturned = query_dict.get('MaxReturned', None)
        self.ModifiedDateRangeFilter = ModifiedDateRangeFilter(**query_dict.get('ModifiedDateRangeFilter', {}))
        self.TxnDateRangeFilter = TxnDateRangeFilter(**query_dict.get('TxnDateRangeFilter', {}))
        self.IncludeRetElements = self.get_include_ret_elements(query_dict.get('IncludeRetElements', []))

    def get_txn_ids(self, txn_ids):
        if isinstance(txn_ids, list):
            return txn_ids
        elif txn_ids:
            return [txn_ids]
        else:
            return []

    def get_include_ret_elements(self, include_ret_elements):
        if isinstance(include_ret_elements, list):
            return include_ret_elements
        elif include_ret_elements:
            return [include_ret_elements]
        else:
            return []

    def to_xml(self):
        root = etree.Element(self.__class__.__name__ + 'Rq')
        if self.TxnIDs:
            for txn_id in self.TxnIDs:
                txn_id_element = etree.Element('TxnID')
                txn_id_element.text = txn_id
                root.append(txn_id_element)
        else:
            if self.MaxReturned:
                max_returned = etree.Element('MaxReturned')
                max_returned.text = self.MaxReturned
                root.append(max_returned)
            else:
                pass

            if self.ModifiedDateRangeFilter:
                modified_date_range_filter = etree.fromstring(self.ModifiedDateRangeFilter.to_xml())
                root.append(modified_date_range_filter)
            elif self.TxnDateRangeFilter:
                txn_date_range_filter = etree.fromstring(self.TxnDateRangeFilter.to_xml())
                root.append(txn_date_range_filter)
            else:
                pass

            if self.TimeTrackingEntityFilter:
                time_tracking_entity_filter = etree.fromstring(self.TimeTrackingEntityFilter.to_xml())
                root.append(time_tracking_entity_filter)
            else:
                pass

            if self.IncludeRetElements:
                for include_ret_element in self.IncludeRetElements:
                    include_ret_element_element = etree.Element('IncludeRetElement')
                    include_ret_element_element.text = include_ret_element
                    root.append(include_ret_element_element)
            else:
                pass
        return etree

class ListQuery:
    def __init__(self, query_dict):
        self.ListIDs = self.get_list_ids(query_dict.get('ListIDs', []))
        self.MaxReturned = query_dict.get('MaxReturned', None)
        self.ModifiedDateRangeFilter = ModifiedDateRangeFilter(**query_dict.get('ModifiedDateRangeFilter', {}))
        self.TxnDateRangeFilter = TxnDateRangeFilter(**query_dict.get('TxnDateRangeFilter', {}))
        self.IncludeRetElements = self.get_include_ret_elements(query_dict.get('IncludeRetElements', []))