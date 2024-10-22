import os
import lxml.etree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
from src.quickbooks_desktop.desktop_to_desktop.models import Base
from src.quickbooks_desktop.desktop_to_desktop.passes.pass_01 import pass_01_transform_qbxml, pass_01_add_to_qb
from src.quickbooks_desktop.desktop_to_desktop.passes.pass_02 import pass_02_transform_qbxml, pass_02_add_to_qb, pass_02_process_response_xml, pass_02_mod_line_groups

if __name__ == '__main__':
    # for testing:
    try:
        os.remove('passes/transaction_mappings.db')
    except Exception as e:
        print(e)
    #end for testing

    os.makedirs('passes', exist_ok=True)
    engine = create_engine('sqlite:///passes/transaction_mappings.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    print('trying begin_session')
    qb.open_connection()
    print('began begin_session')
    qb.begin_session()
    #
    # pass_01_transform_qbxml(session)
    # pass_01_add_to_qb(qb)

    print('begin pass 2')
    pass_02_transform_qbxml(session)
    # pass_02_add_to_qb(qb)
    # pass_02_process_response_xml()
    print('finished pass 2')

    qb.close_qb()