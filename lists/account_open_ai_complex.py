import attr
from datetime import datetime
import xml.etree.ElementTree as ET


@attr.s
class AccountQueryRq:
    meta_data = attr.ib(default=None)
    list_id = attr.ib(factory=list)
    full_name = attr.ib(factory=list)
    max_returned = attr.ib(default=None)
    active_status = attr.ib(default=None)
    from_modified_date = attr.ib(default=None)
    to_modified_date = attr.ib(default=None)
    name_filter = attr.ib(default=None)
    name_range_filter = attr.ib(default=None)
    account_type = attr.ib(factory=list)
    currency_filter = attr.ib(default=None)
    include_ret_element = attr.ib(factory=list)
    owner_id = attr.ib(factory=list)

    def to_xml_string(self):
        data = {}
        for attr_name in attr.fields_dict(self.__class__):
            element_name = attr_name.replace("_", "")
            attr_val = getattr(self, attr_name)
            if attr_val is not None:
                if isinstance(attr_val, datetime):
                    data[element_name] = {"#text": attr_val.strftime("%Y-%m-%dT%H:%M:%S")}
                elif isinstance(attr_val, list):
                    if all(isinstance(i, str) for i in attr_val):
                        data[element_name] = [{"#text": x} for x in attr_val]
                    elif all(isinstance(i, attr.s) for i in attr_val):
                        data[element_name] = [x.to_dict() for x in attr_val]
                elif isinstance(attr_val, attr.s):
                    data[element_name] = attr_val.to_dict()
                else:
                    data[element_name] = {"#text": attr_val}
        xml_string = '<AccountQueryRq>' + dicttoxml.dicttoxml(data, custom_root='AccountQueryRq',
                                                              attr_type=False).decode() + '</AccountQueryRq>'
        return xml_string

    def from_xml_string(cls, xml_string):
        def parse_xml_element(element):
            """Helper function to parse xml elements and convert to python object"""
            attribute_name = '_'.join([w.lower() for w in element.tag.split('}')[-1].split('_')])
            attribute_value = None
            if element.tag == 'ListID':
                attribute_value = element.text
            elif element.tag == 'FullName':
                attribute_value = element.text
            elif element.tag == 'MaxReturned':
                attribute_value = int(element.text)
            elif element.tag == 'ActiveStatus':
                attribute_value = element.text
            elif element.tag == 'FromModifiedDate':
                attribute_value = datetime.strptime(element.text, '%Y-%m-%dT%H:%M:%S')
            elif element.tag == 'ToModifiedDate':
                attribute_value = datetime.strptime(element.text, '%Y-%m-%dT%H:%M:%S')
            elif len(element) > 0:
                attribute_value = {}
                for child in element:
                    attribute_value[child.tag] = parse_xml_element(child)
            return {attribute_name: attribute_value}

        root = ET.fromstring(xml_string)
        data = {}
        for element in root:
            data.update(parse_xml_element(element))

        return cls(**data)

    @classmethod
    def from_dict(cls, data):
        if 'from_modified_date' in data:
            data['from_modified_date'] = datetime.strptime(data['from_modified_date'], '%Y-%m-%dT%H:%M:%S')
        if 'to_modified_date' in data:
            data['to_modified_date'] = datetime.strptime(data['to_modified_date'], '%Y-%m-%dT%H:%M:%S')
        return cls(**data)

    def to_dict(self):
        data = {}
        for key in self.__dict__:
            if key in ["from_modified_date", "to_modified_date"]:
                if self.__dict__[key]:
                    data[key] = self.__dict__[key].strftime('%Y-%m-%dT%H:%M:%S')
                continue
            data[key] = self.__dict__[key]
        return data

    def validate(self):
        errors = {}

        self.validate_meta_data(errors)
        self.validate_active_status(errors)
        self.validate_modified_dates(errors)
        self.validate_name_filter(errors)
        self.validate_account_type(errors)
        self.validate_special_account_type(errors)
        self.validate_currency_filter(errors)

        return errors

    def validate_meta_data(self, errors):
        if self.meta_data is None:
            errors["meta_data"] = "meta_data is required"
        elif self.meta_data not in ["ENUMTYPE"]:
            errors["meta_data"] = "meta_data should be ENUMTYPE"

    def validate_active_status(self, errors):
        if self.active_status is not None and self.active_status not in ["ActiveOnly", "InactiveOnly", "All"]:
            errors["active_status"] = "active_status should be one of [ActiveOnly, InactiveOnly, All]"

    def validate_modified_dates(self, errors):
        if self.from_modified_date is not None and not isinstance(self.from_modified_date, datetime):
            errors["from_modified_date"] = "from_modified_date should be a datetime object"
        if self.to_modified_date is not None and not isinstance(self.to_modified_date, datetime):
            errors["to_modified_date"] = "to_modified_date should be a datetime object"

    def validate_name_filter(self, errors):
        if self.name_filter is not None and self.name_filter.get("MatchCriterion") not in ["StartsWith", "Contains",
                                                                                           "EndsWith"]:
            errors["name_filter"] = "MatchCriterion should be one of [StartsWith, Contains, EndsWith]"

    def validate_account_type(self, errors):
        if self.account_type is not None and self.account_type not in ["AccountsPayable", "AccountsReceivable", "Bank",
                                                                       "CostOfGoodsSold", "CreditCard", "Equity",
                                                                       "Expense", "FixedAsset", "Income",
                                                                       "LongTermLiability", "NonPosting", "OtherAsset",
                                                                       "OtherCurrentAsset", "OtherCurrentLiability",
                                                                       "OtherExpense", "OtherIncome"]:
            errors[
                "account_type"] = "account_type should be one of [AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome]"

    def validate_special_account_type(self, errors):
        if self.special_account_type is not None and self.special_account_type not in ["AccountsPayable",
                                                                                       "AccountsReceivable",
                                                                                       "CondenseItemAdjustmentExpenses",
                                                                                       "CostOfGoodsSold",
                                                                                       "DirectDepositLiabilities",
                                                                                       "Estimates", "ExchangeGainLoss",
                                                                                       "InventoryAssets",
                                                                                       "ItemReceiptAccount",
                                                                                       "OpeningBalanceEquity",
                                                                                       "PayrollExpenses",
                                                                                       "PayrollLiabilities",
                                                                                       "PettyCash", "PurchaseOrders",
                                                                                       "ReconciliationDifferences",
                                                                                       "RetainedEarnings",
                                                                                       "SalesOrders", "SalesTaxPayable",
                                                                                       "UncategorizedExpenses",
                                                                                       "UncategorizedIncome",
                                                                                       "UndepositedFunds"]:
            errors[
                "special_account_type"] = "special_account_type should be one of [AccountsPayable, AccountsReceivable, CondenseItemAdjustmentExpenses, CostOfGoodsSold, DirectDepositLiabilities, Estimates, ExchangeGainLoss, InventoryAssets, ItemReceiptAccount, OpeningBalanceEquity, PayrollExpenses, PayrollLiabilities, PettyCash, PurchaseOrders, ReconciliationDifferences, RetainedEarnings, SalesOrders, SalesTaxPayable, UncategorizedExpenses, UncategorizedIncome, UndepositedFunds]"

    def validate_currency_filter(self, errors):
        if self.currency_filter is not None:
            if self.currency_filter.list_id is not None and not isinstance(self.currency_filter.list_id, str):
                errors["currency_filter.list_id"] = "should be a string"
            if self.currency_filter.full_name is not None and not isinstance(self.currency_filter.full_name, str):
                errors["currency_filter.full_name"] = "should be a string"