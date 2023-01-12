from datetime import datetime
from utility.utilities import from_lxml_elements
from attrs import define

@define
class ARRefundCrediCard:
    TxnID: str = None
    TimeCreated: datetime = None
    TimeModified: datetime = None
    EditSequence: str = None
    TxnNumber: int = None
    CustomerRefListID: str = None
    CustomerRefFullName: str = None
    RefundFromAccountRefListID: str = None
    RefundFromAccountRefFullName: str = None
    ARAccountRefListID: str = None
    ARAccountRefFullName: str = None
    TxnDate: datetime = None
    RefNumber: str = None
    TotalAmount: float = None
    CurrencyRefListID: str = None
    CurrencyRefFullName: str = None
    ExchangeRate: float = None
    TotalAmountInHomeCurrency: float = None
    AddressAddr1: str = None
    AddressAddr2: str = None
    AddressAddr3: str = None
    AddressAddr4: str = None
    AddressAddr5: str = None
    AddressCity: str = None
    AddressState: str = None
    AddressPostalCode: str = None
    AddressCountry: str = None
    AddressNote: str = None
    AddressBlockAddr1: str = None
    AddressBlockAddr2: str = None
    AddressBlockAddr3: str = None
    AddressBlockAddr4: str = None
    AddressBlockAddr5: str = None
    PaymentMethodRefListID: str = None
    PaymentMethodRefFullName: str = None
    Memo: str = None
    CreditCardTxnInfoCreditCardNumberCreditCardNumber: str = None
    CreditCardTxnInfoExpirationMonthExpirationMonth: int = None
    CreditCardTxnInfoExpirationYearExpirationYear: int = None
    CreditCardTxnInfoNameOnCardNameOnCard: str = None
    CreditCardTxnInfoCreditCardAddressCreditCardAddress: str = None
    CreditCardTxnInfoCreditCardPostalCodeCreditCardPostalCode: str = None
    CreditCardTxnInfoCommercialCardCodeCommercialCardCode: str = None
    CreditCardTxnInfoTransactionModeTransactionMode: str = None #todo: validate
    CreditCardTxnInfoCreditCardTxnTypeCreditCardTxnType: str = None #todo: validate
    CreditCardTxnInfoResultCodeResultCode: int = None
    CreditCardTxnInfoResultMessageResultMessage: str = None
    CreditCardTxnInfoCreditCardTransIDCreditCardTransID: str = None
    CreditCardTxnInfoMerchantAccountNumberMerchantAccountNumber: str = None
    CreditCardTxnInfoAuthorizationCodeAuthorizationCode: str = None
    CreditCardTxnInfoAVSStreetAVSStreet: str = None #todo: validate
    CreditCardTxnInfoAVSZipAVSZip: str = None #todo: validate
    CreditCardTxnInfoCardSecurityCodeMatchCardSecurityCodeMatch: str = None #todo: validate
    CreditCardTxnInfoReconBatchIDReconBatchID: str = None
    CreditCardTxnInfoPaymentGroupingCodePaymentGroupingCode: int = None
    CreditCardTxnInfoPaymentStatusPaymentStatus: str = None #todo: validate
    CreditCardTxnInfoTxnAuthorizationStampTxnAuthorizationStamp: int = None
    CreditCardTxnInfoClientTransIDClientTransID: str = None
    ExternalGUID: str = None
    RefundAppliedToTxnRetTxnID: str = None
    RefundAppliedToTxnRetTxnType: str = None #todo: validate
    RefundAppliedToTxnRetTxnDate: datetime = None
    RefundAppliedToTxnRetRefNumber: str = None
    RefundAppliedToTxnRetCreditRemaining: float = None
    RefundAppliedToTxnRetRefundAmount: float = None
    RefundAppliedToTxnRetCreditRemainingInHomeCurrency: float = None
    RefundAppliedToTxnRetRefundAmountInHomeCurrency: float = None
    DataExtRetOwnerID: str = None
    DataExtRetDataExtName: str = None
    DataExtRetDataExtType: str = None #todo: validate
    DataExtRetDataExtValue: str = None

    @classmethod
    def from_xml(cls, elements):
        account = from_lxml_elements(cls, elements, combine_with_child_list=['TaxLineInfoRet', 'CurrencyRef'])
        return account
