from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
import os

def get_pass_00_xml():
    pass_list = [
        'Account',
        'BillingRate',
        'Class',
        'Currency',
        'Customer',
        'CustomerMsg',
        'CustomerType',
        'DateDrivenTerms',
        'Employee',
        'InventorySite',
        'ItemDiscount',
        'ItemFixedAsset',
        'ItemGroup',
        'ItemInventory',
        'ItemInventoryAssembly',
        'ItemNonInventory',
        'ItemOtherCharge',
        'ItemPayment',
        'ItemSalesTax',
        'ItemSalesTaxGroup',
        'ItemService',
        'ItemSubtotal',
        'JobType',
        'OtherName',
        'PaymentMethod',
        'PayrollItemWage',
        'PriceLevel',
        'SalesRep',
        'SalesTaxCode',
        'ShipMethod',
        'StandardTerms',
        'UnitOfMeasureSet',
        'Vehicle',
        'Vendor',
        'VendorType',
        'WorkersCompCode'
    ]

    pass_lists_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <AccountQueryRq requestID="1">
                <ActiveStatus>All</ActiveStatus>
                <OwnerID>0</OwnerID>
            </AccountQueryRq>
            <BillingRateQueryRq requestID="2"></BillingRateQueryRq>
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
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_lists_xml

def get_pass_01_xml():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "JournalEntry",  # because journals can have ap and ar related transactions
    ]
    pass_01_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <TimeTrackingQueryRq requestID="1"></TimeTrackingQueryRq>
            <VehicleMileageQueryRq requestID="2"></VehicleMileageQueryRq>
            <JournalEntryQueryRq requestID="3">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </JournalEntryQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_01_xml

def get_pass_02_xml():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "Estimate",
        "PurchaseOrder",
    ]
    pass_02_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <TimeTrackingQueryRq requestID="1"></TimeTrackingQueryRq>
            <VehicleMileageQueryRq requestID="2"></VehicleMileageQueryRq>
            <EstimateQueryRq requestID="3">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </EstimateQueryRq>
            <PurchaseOrderQueryRq requestID="4">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </PurchaseOrderQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_02_xml

def get_pass_03_xml():
    pass_list = [
        "SalesOrder",
        "ItemReceipt",
    ]
    pass_03_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <SalesOrderQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </SalesOrderQueryRq>
            <ItemReceiptQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </ItemReceiptQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_03_xml

def get_pass_04_xml():
    pass_list = [
        "Bill",
        "VendorCredit",
    ]
    pass_04_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <BillQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </BillQueryRq>
            <VendorCreditQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </VendorCreditQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_04_xml

def get_pass_05_xml():
    pass_list = [
        "BuildAssembly",
    ]
    pass_05_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <BuildAssemblyQueryRq requestID="1">
                <OwnerID>0</OwnerID>
            </BuildAssemblyQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_05_xml

def get_pass_06_xml():
    pass_list = [
        "InventoryAdjustment",
        "TransferInventory",
        "Transfer",  # missing in the original list
    ]
    pass_06_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <InventoryAdjustmentQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </InventoryAdjustmentQueryRq>
            <TransferInventoryQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
            </TransferInventoryQueryRq>
            <TransferQueryRq requestID="3">
            </TransferQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_06_xml

def get_pass_07_xml():
    pass_list = [
        "Invoice",
        "SalesReceipt",
    ]
    pass_07_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <InvoiceQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </InvoiceQueryRq>
            <SalesReceiptQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </SalesReceiptQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_07_xml

def get_pass_08_xml():
    pass_list = [
        "CreditMemo",
        "ARRefundCreditCard",
        "ReceivePayment",
        "Deposit",
    ]
    pass_08_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <CreditMemoQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </CreditMemoQueryRq>
            <ARRefundCreditCardQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </ARRefundCreditCardQueryRq>
            <ReceivePaymentQueryRq requestID="3">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </ReceivePaymentQueryRq>
            <DepositQueryRq requestID="4">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </DepositQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_08_xml

def get_pass_09_xml():
    pass_list = [
        "Charge",  # because sometimes they have ap accounts and need to be referenced
        "Check",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCharge",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCredit",
    ]
    pass_09_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <ChargeQueryRq requestID="1">
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </ChargeQueryRq>
            <CheckQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <IncludeLinkedTxns>true</IncludeLinkedTxns>
                <OwnerID>0</OwnerID>
            </CheckQueryRq>
            <CreditCardChargeQueryRq requestID="3">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </CreditCardChargeQueryRq>
            <CreditCardCreditQueryRq requestID="4">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </CreditCardCreditQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_09_xml

def get_pass_10_xml():
    pass_list = [
        "BillPaymentCheck",
        "BillPaymentCreditCard",
        "SalesTaxPaymentCheck",
    ]
    pass_10_xml = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="continueOnError">
            <BillPaymentCheckQueryRq requestID="1">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </BillPaymentCheckQueryRq>
            <BillPaymentCreditCardQueryRq requestID="2">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </BillPaymentCreditCardQueryRq>
            <SalesTaxPaymentCheckQueryRq requestID="3">
                <IncludeLineItems>true</IncludeLineItems>
                <OwnerID>0</OwnerID>
            </SalesTaxPaymentCheckQueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    return pass_10_xml

def get_all_data():
    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    pass_xml_functions = [
        get_pass_00_xml,
        get_pass_01_xml,
        get_pass_02_xml,
        get_pass_03_xml,
        get_pass_04_xml,
        get_pass_05_xml,
        get_pass_06_xml,
        get_pass_07_xml,
        get_pass_08_xml,
        get_pass_09_xml,
        get_pass_10_xml
    ]
    qb.open_connection()
    print('trying begin_session')
    qb.begin_session()
    print('began begin_session')
    for i, get_pass_xml in enumerate(pass_xml_functions):
        if i <= 0:
            pass
        else:
            try:
                xml_str = get_pass_xml()
                print(i)
                response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
                folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_xml")
                os.makedirs(folder_path, exist_ok=True)
                response_file_path = os.path.join(folder_path, f'response_pass_{i:02d}.xml')
                with open(response_file_path, 'w') as response_file:
                    response_file.write(response)
            except Exception as e:
                print(e)
    qb.close_qb()

if __name__ == '__main__':
    get_all_data()
