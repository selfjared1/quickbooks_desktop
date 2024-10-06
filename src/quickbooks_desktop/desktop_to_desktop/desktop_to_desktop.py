from src.quickbooks_desktop.desktop_to_desktop.query_all import query_all
import os
from burn.phone_notifications import notify_jared_process_is_done

#Info on things that need to be done manually:
    #Add currency exchange rates
def transfer_lists():
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

def pass_01():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "JournalEntry",  # because journals can have ap and ar related transactions
    ]

def pass_02():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "Estimate",
        "PurchaseOrder",
    ]

def pass_03():
    pass_list = [
        "SalesOrder",
        "ItemReceipt",
    ]

def pass_04():
    # because you purchase stuff before you can sell it
    pass_list = [
        "Bill",
        "VendorCredit",
    ]

def pass_05():
    # because you build stuff after you purchase it
    pass_list = [
        "BuildAssembly",
        "BuildAssemblyPending",  # missing in the original list
    ]

def pass_06():
    # because you adjust then transfer inventory before you sell it
    pass_list = [
        "InventoryAdjustment",
        "TransferInventory",
        "Transfer",  # missing in the original list
    ]

def pass_07():
    # sell stuff
    pass_list = [
        "Invoice",
        "SalesReceipt",
    ]

def pass_08():
    # get paid
    pass_list = [
        "CreditMemo",
        "ARRefundCreditCard",
        "ReceivePayment",
        "Deposit",
    ]

def pass_09():
    # spend money after you get paid
    pass_list = [
        "Charge",  # because sometimes they have ap accounts and need to be referenced
        "Check",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCharge",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCredit",
    ]

def pass_10():
    # pay bills
    pass_list = [
        "BillPaymentCheck",
        "BillPaymentCreditCard",
        "SalesTaxPaymentCheck",
    ]

def main():
    file_location = os.path.expanduser("~/Desktop/burn")
    response_file_path = os.path.join(file_location, f"full_file.xml")
    query_all(response_file_path)
    notify_jared_process_is_done()


if __name__ == '__main__':
    main()





