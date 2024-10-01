from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
from src.quickbooks_desktop.lists.currency import Currency
from src.quickbooks_desktop.conversions import qb_to_sql, sql_to_qb

def get_currency():
    qb = QuickbooksDesktop()
    currency_query = Currency.Query()
    query_xml = currency_query.to_xml()
    response = qb.send_xml(query_xml)
    print(response)


if __name__ == '__main__':
    get_currency()