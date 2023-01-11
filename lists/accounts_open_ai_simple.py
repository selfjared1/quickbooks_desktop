import attr
import xmltodict
import re
from utility import camel_to_snake_str, snake_to_camel_str

@attr.s
class AccountRet:
    list_id = attr.ib(type=str, default=None)
    time_created = attr.ib(type=str, default=None)
    time_modified = attr.ib(type=str, default=None)
    edit_sequence = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    full_name = attr.ib(type=str, default=None)
    is_active = attr.ib(type=bool, default=None)
    sublevel = attr.ib(type=int, default=None)
    account_type = attr.ib(type=str, default=None)
    special_account_type = attr.ib(type=str, default=None)
    account_number = attr.ib(type=str, default=None)
    bank_number = attr.ib(type=str, default=None)
    desc = attr.ib(type=str, default=None)
    balance = attr.ib(type=str, default=None)
    total_balance = attr.ib(type=str, default=None)
    cash_flow_classification = attr.ib(type=str, default=None)
    parent_ref = attr.ib(type=object, default=None, repr=False)
    tax_line_info_ret = attr.ib(type=object, default=None, repr=False)
    currency_ref = attr.ib(type=object, default=None, repr=False)
    data_ext_ret = attr.ib(type=object, default=None, repr=False)


@attr.s
class ParentRef:
    list_id = attr.ib(type=str, default=None)
    full_name = attr.ib(type=str, default=None)


@attr.s
class TaxLineInfoRet:
    tax_line_id = attr.ib(type=int, default=None)
    tax_line_name = attr.ib(type=str, default=None)


@attr.s
class CurrencyRef:
    list_id = attr.ib(type=str, default=None)
    full_name = attr.ib(type=str, default=None)


@attr.s
class DataExtRet:
    owner_id = attr.ib(type=str, default=None)
    data_ext_name = attr.ib(type=str, default=None)
    data_ext_type = attr.ib(type=str, default=None)
    data_ext_value = attr.ib(type=str, default=None)


def from_xml_string(xml_string):
    xml_dict = xmltodict.parse(xml_string)['AccountRet']
    parent_ref = ParentRef(**{camel_to_snake_str(key): value for key, value in
                              xml_dict.pop('ParentRef').items()}) if 'ParentRef' in xml_dict else None
    tax_line_info_ret = TaxLineInfoRet(**{camel_to_snake_str(key): value for key, value in xml_dict.pop(
        'TaxLineInfoRet').items()}) if 'TaxLineInfoRet' in xml_dict else None
    currency_ref = CurrencyRef(**{camel_to_snake_str(key): value for key, value in
                                  xml_dict.pop('CurrencyRef').items()}) if 'CurrencyRef' in xml_dict else None
    data_ext_ret = DataExtRet(**{camel_to_snake_str(key): value for key, value in
                                 xml_dict.pop('DataExtRet').items()}) if 'DataExtRet' in xml_dict else None
    kwargs = {camel_to_snake_str(key): value for key, value in xml_dict.items()}
    return AccountRet(parent_ref=parent_ref, tax_line_info_ret=tax_line_info_ret, currency_ref=currency_ref,
                      data_ext_ret=data_ext_ret, **kwargs)


def to_xml_string(account_ret: AccountRet):
    data = {}
    for attr in vars(account_ret):
        if attr in ['parent_ref', 'tax_line_info_ret', 'currency_ref', 'data_ext_ret']:
            data[snake_to_camel_str(attr)] = vars(getattr(account_ret, attr))
        else:
            data[snake_to_camel_str(attr)] = getattr(account_ret, attr)
    return xmltodict.unparse({'AccountRet': data}, pretty=True)

xml_str = """
    <AccountRet>
      <ListID>1234567890</ListID>
      <TimeCreated>2022-12-31T23:59:59-07:00</TimeCreated>
      <TimeModified>2022-12-31T23:59:59-07:00</TimeModified>
      <EditSequence>abcdefghijk</EditSequence>
      <Name>Sample Account</Name>
      <FullName>Sample Account</FullName>
      <IsActive>true</IsActive>
      <ParentRef>
        <ListID>0987654321</ListID>
        <FullName>Parent Account</FullName>
      </ParentRef>
      <Sublevel>0</Sublevel>
      <AccountType>Checking</AccountType>
      <SpecialAccountType>Regular</SpecialAccountType>
      <AccountNumber>12345</AccountNumber>
      <BankNumber>67890</BankNumber>
      <Desc>This is a sample account</Desc>
      <Balance>1000.00</Balance>
      <TotalBalance>1000.00</TotalBalance>
      <TaxLineInfoRet>
        <TaxLineID>1</TaxLineID>
        <TaxLineName>Sales Tax</TaxLineName>
      </TaxLineInfoRet>
      <CashFlowClassification>Operating</CashFlowClassification>
      <CurrencyRef>
        <ListID>USD</ListID>
        <FullName>US Dollar</FullName>
      </CurrencyRef>
      <DataExtRet>
        <OwnerID>01234567-89ab-cdef-0123-4567890abcde</OwnerID>
        <DataExtName>Extension 1</DataExtName>
        <DataExtType>String</DataExtType>
        <DataExtValue>Some additional information</DataExtValue>
      </DataExtRet>
    </AccountRet>
"""

if __name__ == '__main__':
    account_ret = from_xml_string(xml_str)
    print(account_ret)
    xml_string = to_xml_string(account_ret)
    print(xml_str == xml_string)
    print('i')