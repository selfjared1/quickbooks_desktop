import os
from src.quickbooks_desktop.desktop_to_desktop.resources_dict import get_list_of_lists, get_list_of_transactions
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop

def build_queries():
    list_of_lists = get_list_of_lists()
    queries = ''
    request_id = 1
    for list_table in list_of_lists:
        query = f"""<{list_table}QueryRq requestID="{request_id}">
                <ActiveStatus>All</ActiveStatus>
                <OwnerID>0</OwnerID>
            </{list_table}QueryRq>"""
        queries += query
        request_id += 1

    transactions_list = get_list_of_transactions()
    for transaction_table in transactions_list:
        query = f"""<{transaction_table}QueryRq requestID="{request_id}">
                        <IncludeLineItems>true</IncludeLineItems>
                        <IncludeLinkedTxns>true</IncludeLinkedTxns>
                        <OwnerID>0</OwnerID>
                    </{transaction_table}QueryRq>"""
        queries += query
        request_id += 1
    return queries




def query_all(response_file_path):

    xml_str = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="continueOnError">
                <AccountQueryRq requestID="1">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </AccountQueryRq>
                <BillingRateQueryRq requestID="2">
                </BillingRateQueryRq>
                <ClassQueryRq requestID="3">
                    <ActiveStatus>All</ActiveStatus>
                </ClassQueryRq>
                <CurrencyQueryRq requestID="4">
                    <ActiveStatus>All</ActiveStatus>
                </CurrencyQueryRq>
                <CustomerQueryRq requestID="5">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </CustomerQueryRq>
                <CustomerMsgQueryRq requestID="6">
                    <ActiveStatus>All</ActiveStatus>
                </CustomerMsgQueryRq>
                <CustomerTypeQueryRq requestID="7">
                    <ActiveStatus>All</ActiveStatus>
                </CustomerTypeQueryRq>
                <DateDrivenTermsQueryRq requestID="8">
                    <ActiveStatus>All</ActiveStatus>
                </DateDrivenTermsQueryRq>
                <EmployeeQueryRq requestID="9">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </EmployeeQueryRq>
                <InventorySiteQueryRq requestID="10">
                    <ActiveStatus>All</ActiveStatus>
                </InventorySiteQueryRq>
                <ItemDiscountQueryRq requestID="11">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemDiscountQueryRq>
                <ItemFixedAssetQueryRq requestID="12">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemFixedAssetQueryRq>
                <ItemGroupQueryRq requestID="13">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemGroupQueryRq>
                <ItemInventoryQueryRq requestID="14">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemInventoryQueryRq>
                <ItemInventoryAssemblyQueryRq requestID="15">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemInventoryAssemblyQueryRq>
                <ItemNonInventoryQueryRq requestID="16">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemNonInventoryQueryRq>
                <ItemOtherChargeQueryRq requestID="17">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemOtherChargeQueryRq>
                <ItemPaymentQueryRq requestID="18">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemPaymentQueryRq>
                <ItemSalesTaxQueryRq requestID="19">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemSalesTaxQueryRq>
                <ItemSalesTaxGroupQueryRq requestID="20">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemSalesTaxGroupQueryRq>
                <ItemServiceQueryRq requestID="21">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemServiceQueryRq>
                <ItemSubtotalQueryRq requestID="22">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </ItemSubtotalQueryRq>
                <JobTypeQueryRq requestID="23">
                    <ActiveStatus>All</ActiveStatus>
                </JobTypeQueryRq>
                <OtherNameQueryRq requestID="24">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </OtherNameQueryRq>
                <PaymentMethodQueryRq requestID="25">
                    <ActiveStatus>All</ActiveStatus>
                </PaymentMethodQueryRq>
                <PayrollItemWageQueryRq requestID="26">
                    <ActiveStatus>All</ActiveStatus>
                </PayrollItemWageQueryRq>
                <PriceLevelQueryRq requestID="27">
                    <ActiveStatus>All</ActiveStatus>
                </PriceLevelQueryRq>
                <SalesRepQueryRq requestID="28">
                    <ActiveStatus>All</ActiveStatus>
                </SalesRepQueryRq>
                <SalesTaxCodeQueryRq requestID="29">
                    <ActiveStatus>All</ActiveStatus>
                </SalesTaxCodeQueryRq>
                <ShipMethodQueryRq requestID="30">
                    <ActiveStatus>All</ActiveStatus>
                </ShipMethodQueryRq>
                <StandardTermsQueryRq requestID="31">
                    <ActiveStatus>All</ActiveStatus>
                </StandardTermsQueryRq>
                <UnitOfMeasureSetQueryRq requestID="32">
                    <ActiveStatus>All</ActiveStatus>
                </UnitOfMeasureSetQueryRq>
                <VehicleQueryRq requestID="33">
                    <ActiveStatus>All</ActiveStatus>
                </VehicleQueryRq>
                <VendorQueryRq requestID="34">
                    <ActiveStatus>All</ActiveStatus>
                    <OwnerID>0</OwnerID>
                </VendorQueryRq>
                <VendorTypeQueryRq requestID="35">
                    <ActiveStatus>All</ActiveStatus>
                </VendorTypeQueryRq>
                <WorkersCompCodeQueryRq requestID="36">
                    <ActiveStatus>All</ActiveStatus>
                </WorkersCompCodeQueryRq>
                <ARRefundCreditCardQueryRq requestID="37">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </ARRefundCreditCardQueryRq>
                <BillQueryRq requestID="38">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </BillQueryRq>
                <BillPaymentCheckQueryRq requestID="39">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </BillPaymentCheckQueryRq>
                <BillPaymentCreditCardQueryRq requestID="40">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </BillPaymentCreditCardQueryRq>
                <BuildAssemblyQueryRq requestID="41">
                    <OwnerID>0</OwnerID>
                </BuildAssemblyQueryRq>
                <ChargeQueryRq requestID="43">
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </ChargeQueryRq>
                <CheckQueryRq requestID="44">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </CheckQueryRq>
                <CreditCardChargeQueryRq requestID="45">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </CreditCardChargeQueryRq>
                <CreditCardCreditQueryRq requestID="46">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </CreditCardCreditQueryRq>
                <CreditMemoQueryRq requestID="47">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </CreditMemoQueryRq>
                <DepositQueryRq requestID="48">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </DepositQueryRq>
                <EstimateQueryRq requestID="49">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </EstimateQueryRq>
                <InventoryAdjustmentQueryRq requestID="50">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </InventoryAdjustmentQueryRq>
                <InvoiceQueryRq requestID="51">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </InvoiceQueryRq>
                <ItemReceiptQueryRq requestID="52">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </ItemReceiptQueryRq>
                <JournalEntryQueryRq requestID="53">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </JournalEntryQueryRq>
                <PurchaseOrderQueryRq requestID="54">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </PurchaseOrderQueryRq>
                <ReceivePaymentQueryRq requestID="55">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </ReceivePaymentQueryRq>
                <SalesOrderQueryRq requestID="56">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </SalesOrderQueryRq>
                <SalesReceiptQueryRq requestID="57">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </SalesReceiptQueryRq>
                <SalesTaxPaymentCheckQueryRq requestID="58">
                    <IncludeLineItems>true</IncludeLineItems>
                    <OwnerID>0</OwnerID>
                </SalesTaxPaymentCheckQueryRq>
                <TimeTrackingQueryRq requestID="59">
                </TimeTrackingQueryRq>
                <TransferQueryRq requestID="60">
                </TransferQueryRq>
                <TransferInventoryQueryRq requestID="61">
                    <IncludeLineItems>true</IncludeLineItems>
                </TransferInventoryQueryRq>
                <VehicleMileageQueryRq requestID="62">
                </VehicleMileageQueryRq>
                <VendorCreditQueryRq requestID="63">
                    <IncludeLineItems>true</IncludeLineItems>
                    <IncludeLinkedTxns>true</IncludeLinkedTxns>
                    <OwnerID>0</OwnerID>
                </VendorCreditQueryRq>
            </QBXMLMsgsRq>
        </QBXML>"""


    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    print('trying begin_session')
    qb.begin_session()
    print('began begin_session')
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)

        with open(response_file_path, 'w') as response_file:
            response_file.write(response)
    except Exception as e:
        print(e)
    qb.close_qb()


def query_all_old(response_file_path):
    queries = build_queries()
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
                        <QBXML>
                            <QBXMLMsgsRq onError="stopOnError">
                                {queries}
                            </QBXMLMsgsRq>
                        </QBXML>"""
    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)

        with open(response_file_path, 'w') as response_file:
            response_file.write(response)
    except Exception as e:
        print(e)
    qb.close_qb()



