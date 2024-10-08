from src.quickbooks_desktop.desktop_to_desktop.models import TransactionMapping
from src.quickbooks_desktop.desktop_to_desktop.utilities import add_journal_line_to_db, add_line_ret_to_db


def add_rq_to_db(qbxml_msgs, session):
    # print('began add_rq_to_db')
    # print(len(qbxml_msgs))
    loop_num = len(qbxml_msgs)
    print(f'looping {loop_num}')
    for i in range(loop_num):
        print(i)
        rq_element = qbxml_msgs[i]
        request_id = int(rq_element.get('requestID', '0'))
        qb_table_name = rq_element.tag.replace('Rq', '')
        add_element = rq_element[0] if len(rq_element) > 0 else None
        first_child = add_element[0] if len(add_element) > 0 else None
        if first_child is not None and first_child.tag == 'TxnID':
            # print('begain first_child')
            old_qb_trx_id = first_child.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                old_qb_trx_id=old_qb_trx_id
            )
            session.add(mapping)
            first_child.getparent().remove(first_child)
            # print('begin add_journal_line_to_db')
            add_journal_line_to_db(add_element, request_id, qb_table_name, old_qb_trx_id, session)

            # print('begin add_line_ret_to_db')
            add_line_ret_to_db(add_element, request_id, qb_table_name, old_qb_trx_id, session)
            # print('end add_line_ret_to_db')
        else:
            print('need to figure out how to get old trx_id')
            pass

    session.commit()
    print('end add_rq_to_db')
