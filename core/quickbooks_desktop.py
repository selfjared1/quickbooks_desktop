from core.session_manager import SessionManager
from lxml import etree as et
import pandas as pd
import sqlite3
import xmltodict

available_actions = [
'ARRefundCreditCardAdd',
'ARRefundCreditCardQuery',
'AccountAdd',
'AccountMod',
'AccountQuery',
'AccountTaxLineInfoQuery',
'AgingReportQuery',
'BarCodeQuery',
'BillAdd',
'BillMod',
'BillPaymentCheckAdd',
'BillPaymentCheckMod',
'BillPaymentCheckQuery',
'BillPaymentCreditCardAdd',
'BillPaymentCreditCardQuery',
'BillQuery',
'BillToPayQuery',
'BillingRateAdd',
'BillingRateQuery',
'BudgetSummaryReportQuery',
'BuildAssemblyAdd',
'BuildAssemblyMod',
'BuildAssemblyQuery',
'ChargeAdd',
'ChargeMod',
'ChargeQuery',
'CheckAdd',
'CheckMod',
'CheckQuery',
'ClassAdd',
'ClassMod',
'ClassQuery',
'ClearedStatusMod',
'CompanyActivityQuery',
'CompanyQuery',
'CreditCardChargeAdd',
'CreditCardChargeMod',
'CreditCardChargeQuery',
'CreditCardCreditAdd',
'CreditCardCreditMod',
'CreditCardCreditQuery',
'CreditMemoAdd',
'CreditMemoMod',
'CreditMemoQuery',
'CurrencyAdd',
'CurrencyMod',
'CurrencyQuery',
'CustomDetailReportQuery',
'CustomSummaryReportQuery',
'CustomerAdd',
'CustomerMod',
'CustomerMsgAdd',
'CustomerMsgQuery',
'CustomerQuery',
'CustomerTypeAdd',
'CustomerTypeQuery',
'DataEventRecoveryInfoDel',
'DataEventRecoveryInfoQuery',
'DataExtAdd',
'DataExtDefAdd',
'DataExtDefDel',
'DataExtDefMod',
'DataExtDefQuery',
'DataExtDel',
'DataExtMod',
'DateDrivenTermsAdd',
'DateDrivenTermsQuery',
'DepositAdd',
'DepositMod',
'DepositQuery',
'EmployeeAdd',
'EmployeeMod',
'EmployeeQuery',
'EntityQuery',
'EstimateAdd',
'EstimateMod',
'EstimateQuery',
'Form1099CategoryAccountMappingMod',
'Form1099CategoryAccountMappingQuery',
'GeneralDetailReportQuery',
'GeneralSummaryReportQuery',
'HostQuery',
'InventoryAdjustmentAdd',
'InventoryAdjustmentMod',
'InventoryAdjustmentQuery',
'InventorySiteAdd',
'InventorySiteMod',
'InventorySiteQuery',
'InvoiceAdd',
'InvoiceMod',
'InvoiceQuery',
'ItemAssembliesCanBuildQuery',
'ItemDiscountAdd',
'ItemDiscountMod',
'ItemDiscountQuery',
'ItemFixedAssetAdd',
'ItemFixedAssetMod',
'ItemFixedAssetQuery',
'ItemGroupAdd',
'ItemGroupMod',
'ItemGroupQuery',
'ItemInventoryAdd',
'ItemInventoryAssemblyAdd',
'ItemInventoryAssemblyMod',
'ItemInventoryAssemblyQuery',
'ItemInventoryMod',
'ItemInventoryQuery',
'ItemNonInventoryAdd',
'ItemNonInventoryMod',
'ItemNonInventoryQuery',
'ItemOtherChargeAdd',
'ItemOtherChargeMod',
'ItemOtherChargeQuery',
'ItemPaymentAdd',
'ItemPaymentMod',
'ItemPaymentQuery',
'ItemQuery',
'ItemReceiptAdd',
'ItemReceiptMod',
'ItemReceiptQuery',
'ItemSalesTaxAdd',
'ItemSalesTaxGroupAdd',
'ItemSalesTaxGroupMod',
'ItemSalesTaxGroupQuery',
'ItemSalesTaxMod',
'ItemSalesTaxQuery',
'ItemServiceAdd',
'ItemServiceMod',
'ItemServiceQuery',
'ItemSitesQuery',
'ItemSubtotalAdd',
'ItemSubtotalMod',
'ItemSubtotalQuery',
'JobReportQuery',
'JobTypeAdd',
'JobTypeQuery',
'JournalEntryAdd',
'JournalEntryMod',
'JournalEntryQuery',
'LeadAdd',
'LeadMod',
'LeadQuery',
'ListDel',
'ListDeletedQuery',
'ListDisplayAdd',
'ListDisplayMod',
'ListMerge',
'OtherNameAdd',
'OtherNameMod',
'OtherNameQuery',
'PaymentMethodAdd',
'PaymentMethodQuery',
'PayrollDetailReportQuery',
'PayrollItemNonWageQuery',
'PayrollItemWageAdd',
'PayrollItemWageQuery',
'PayrollSummaryReportQuery',
'PreferencesQuery',
'PriceLevelAdd',
'PriceLevelMod',
'PriceLevelQuery',
'PurchaseOrderAdd',
'PurchaseOrderMod',
'PurchaseOrderQuery',
'ReceivePaymentAdd',
'ReceivePaymentMod',
'ReceivePaymentQuery',
'ReceivePaymentToDepositQuery',
'SalesOrderAdd',
'SalesOrderMod',
'SalesOrderQuery',
'SalesReceiptAdd',
'SalesReceiptMod',
'SalesReceiptQuery',
'SalesRepAdd',
'SalesRepMod',
'SalesRepQuery',
'SalesTaxCodeAdd',
'SalesTaxCodeMod',
'SalesTaxCodeQuery',
'SalesTaxPayableQuery',
'SalesTaxPaymentCheckAdd',
'SalesTaxPaymentCheckMod',
'SalesTaxPaymentCheckQuery',
'ShipMethodAdd',
'ShipMethodQuery',
'SpecialAccountAdd',
'SpecialItemAdd',
'StandardTermsAdd',
'StandardTermsQuery',
'TemplateQuery',
'TermsQuery',
'TimeReportQuery',
'TimeTrackingAdd',
'TimeTrackingMod',
'TimeTrackingQuery',
'ToDoAdd',
'ToDoMod',
'ToDoQuery',
'TransactionQuery',
'TransferAdd',
'TransferInventoryAdd',
'TransferInventoryMod',
'TransferInventoryQuery',
'TransferMod',
'TransferQuery',
'TxnDel',
'TxnDeletedQuery',
'TxnDisplayAdd',
'TxnDisplayMod',
'TxnVoid',
'UnitOfMeasureSetAdd',
'UnitOfMeasureSetQuery',
'VehicleAdd',
'VehicleMileageAdd',
'VehicleMileageQuery',
'VehicleMod',
'VehicleQuery',
'VendorAdd',
'VendorCreditAdd',
'VendorCreditMod',
'VendorCreditQuery',
'VendorMod',
'VendorQuery',
'VendorTypeAdd',
'VendorTypeQuery',
'WorkersCompCodeAdd',
'WorkersCompCodeMod',
'WorkersCompCodeQuery',
]

class QuickBooksDesktop(SessionManager):
    """
    To do everything in QBD

    """
    def __init__(self):
        self.report = {
            'aging_report_query': 'AgingReportQuery',
            'budget_summary_report_query':'BudgetSummaryReportQuery',
            'custom_detail_report_query': 'CustomDetailReportQuery',
            'custom_summary_report_query': 'CustomSummaryReportQuery',
            'general_detail_report_query':'GeneralDetailReportQuery',
            'general_summary_report_query':'GeneralSummaryReportQuery',
            'job_report_query':'JobReportQuery',
            'payroll_detail_report_query':'PayrollDetailReportQuery',
            'payroll_summary_report_query':'PayrollSummaryReportQuery',
            'time_report_query':'TimeReportQuery'
        }
        self.removed_queries = {
            'bill_to_pay_query': 'BillToPayQuery',
            'data_event_recovery_info_query': 'DataEventRecoveryInfoQuery',
            'item_assemblies_can_build_query':'ItemAssembliesCanBuildQuery',
            'list_deleted_query':'ListDeletedQuery',
            'txn_deleted_query':'TxnDeletedQuery',
        }
        self.query = {
            'ar_refund_credit_card_query':'ARRefundCreditCardQuery',
            'account_query':'AccountQuery',
            'account_tax_line_info_query':'AccountTaxLineInfoQuery',
            'bar_code_query':'BarCodeQuery',
            'bill_payment_check_query':'BillPaymentCheckQuery',
            'bill_payment_credit_card_query':'BillPaymentCreditCardQuery',
            'bill_query':'BillQuery',
            'billing_rate_query':'BillingRateQuery',
            'build_assembly_query':'BuildAssemblyQuery',
            'charge_query':'ChargeQuery',
            'check_query':'CheckQuery',
            'class_query':'ClassQuery',
            'company_activity_query':'CompanyActivityQuery',
            'company_query':'CompanyQuery',
            'credit_card_charge_query':'CreditCardChargeQuery',
            'credit_card_credit_query':'CreditCardCreditQuery',
            'credit_memo_query':'CreditMemoQuery',
            'currency_query':'CurrencyQuery',
            'customer_msg_query':'CustomerMsgQuery',
            'customer_query':'CustomerQuery',
            'customer_type_query':'CustomerTypeQuery',
            'data_ext_def_query':'DataExtDefQuery',
            'date_driven_terms_query':'DateDrivenTermsQuery',
            'deposit_query':'DepositQuery',
            'employee_query':'EmployeeQuery',
            'entity_query':'EntityQuery',
            'estimate_query':'EstimateQuery',
            'form1099_category_account_mapping_query':'Form1099CategoryAccountMappingQuery',
            'host_query':'HostQuery',
            'inventory_adjustment_query':'InventoryAdjustmentQuery',
            'inventory_site_query':'InventorySiteQuery',
            'invoice_query':'InvoiceQuery',
            'item_discount_query':'ItemDiscountQuery',
            'item_fixed_asset_query':'ItemFixedAssetQuery',
            'item_group_query':'ItemGroupQuery',
            'item_inventory_assembly_query':'ItemInventoryAssemblyQuery',
            'item_inventory_query':'ItemInventoryQuery',
            'item_non_inventory_query':'ItemNonInventoryQuery',
            'item_other_charge_query':'ItemOtherChargeQuery',
            'item_payment_query':'ItemPaymentQuery',
            'item_query':'ItemQuery',
            'item_receipt_query':'ItemReceiptQuery',
            'item_sales_tax_group_query':'ItemSalesTaxGroupQuery',
            'item_sales_tax_query':'ItemSalesTaxQuery',
            'item_service_query':'ItemServiceQuery',
            'item_sites_query':'ItemSitesQuery',
            'item_subtotal_query':'ItemSubtotalQuery',
            'job_type_query':'JobTypeQuery',
            'journal_entry_query':'JournalEntryQuery',
            'lead_query':'LeadQuery',
            'other_name_query':'OtherNameQuery',
            'payment_method_query':'PaymentMethodQuery',
            'payroll_item_non_wage_query':'PayrollItemNonWageQuery',
            'payroll_item_wage_query':'PayrollItemWageQuery',
            'preferences_query':'PreferencesQuery',
            'price_level_query':'PriceLevelQuery',
            'purchase_order_query':'PurchaseOrderQuery',
            'receive_payment_query':'ReceivePaymentQuery',
            'receive_payment_to_deposit_query':'ReceivePaymentToDepositQuery',
            'sales_order_query':'SalesOrderQuery',
            'sales_receipt_query':'SalesReceiptQuery',
            'sales_rep_query':'SalesRepQuery',
            'sales_tax_code_query':'SalesTaxCodeQuery',
            'sales_tax_payable_query':'SalesTaxPayableQuery',
            'sales_tax_payment_check_query':'SalesTaxPaymentCheckQuery',
            'ship_method_query':'ShipMethodQuery',
            'standard_terms_query':'StandardTermsQuery',
            'template_query':'TemplateQuery',
            'terms_query':'TermsQuery',
            'time_tracking_query':'TimeTrackingQuery',
            'to_do_query':'ToDoQuery',
            'transaction_query':'TransactionQuery',
            'transfer_inventory_query':'TransferInventoryQuery',
            'transfer_query':'TransferQuery',
            'unit_of_measure_set_query':'UnitOfMeasureSetQuery',
            'vehicle_mileage_query':'VehicleMileageQuery',
            'vehicle_query':'VehicleQuery',
            'vendor_credit_query':'VendorCreditQuery',
            'vendor_query':'VendorQuery',
            'vendor_type_query':'VendorTypeQuery',
            'workers_comp_code_query':'WorkersCompCodeQuery',
            }

    def get_table(self, table_name):
        print(f'begin {table_name}')
        root = et.Element(table_name + 'Rq')
        qb = SessionManager()
        response = qb.send_xml(root)
        xpath = f'''/QBXML/QBXMLMsgsRs/{table_name}Rs/{table_name.replace('Query', '')}Ret'''
        tree = et.fromstring(response)
        tree = tree.xpath(xpath)
        print(table_name)
        # o = untangle.parse(et.tostring(tree[0], encoding='unicode'))
        try:
            df = pd.read_xml(response, xpath, parser='lxml')
            return df
        except Exception as e:
            print(e)
            return None

    def replicate(self):
        connection = sqlite3.connect('qb_data.db')
        for code in self.query.keys():
            df = self.get_table(self.query[code])
            if df is not None:
                df.to_sql(code, connection, if_exists='replace', index=False)

    def generate_xml_files(self):
        for table_name in self.query.keys():
            print(f'begin {table_name}')
            root = et.Element(table_name + 'Rq')
            qb = SessionManager()
            response = qb.send_xml(root)
            try:
                with open(f"{table_name}.xml", "wb") as xml_writer:
                    xml_writer.write(response)
            except IOError:
                pass

if __name__ == '__main__':
    qb = QuickBooksDesktop()
    # qb.replicate()
    df = qb.get_table('BillQuery')

    print('b')
