from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class PaymentMethodRef(QBRefMixin):

    class Meta:
        name = "PaymentMethodRef"