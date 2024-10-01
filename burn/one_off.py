import lxml as et
from quickbooks_desktop.session_manager import SessionManager


def main():
    qb = SessionManager()
    xml_str = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CurrencyQueryRq requestID="1">

        </CurrencyQueryRq>
    </QBXMLMsgsRq>
</QBXML>"""
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
    qb.close_qb()
    print(response)


if __name__ == '__main__':
    main()

