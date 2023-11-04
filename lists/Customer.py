from typing import Optional
import attr
from core.special_fields import QBDate, Ref
from core.base import QBListBase, QBContactBase, QBTransactionBase, QBAddress


@attr.s(auto_attribs=True)
class QBCustomer(QBContactBase):
    Sublevel: Optional[int] = None
    ParentRef: Optional[Ref] = None
    BillAddress: Optional[QBAddress] = None
    ShipAddress: Optional[QBAddress] = None
    CustomerTypeRef: Optional[Ref] = None
    TermsRef: Optional[Ref] = None
    SalesRepRef: Optional[Ref] = None
    Balance: Optional[str] = None
    TotalBalance: Optional[str] = None
    SalesTaxCodeRef: Optional[Ref] = None
    ItemSalesTaxRef: Optional[Ref] = None
    ResaleNumber: Optional[str] = None
    JobStatus: Optional[str] = None
    JobStartDate: Optional[QBDate] = None
    JobProjectedEndDate: Optional[QBDate] = None
    JobEndDate: Optional[QBDate] = None
    JobDesc: Optional[str] = None
    JobTypeRef: Optional[Ref] = None
    PreferredDeliveryMethod: Optional[str] = None
    PriceLevelRef: Optional[Ref] = None
    CreditLimit: Optional[str] = None
    PreferredPaymentMethodRef: Optional[Ref] = None
    # CreditCardInfo: Optional[CreditCardInfo] = None
    CurrencyRef: Optional[Ref] = None
    TaxRegistrationNumber: Optional[str] = None