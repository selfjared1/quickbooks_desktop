from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class CustomerSalesTaxCodeRef(QBRefMixin):

    class Meta:
        name = "CustomerSalesTaxCodeRef"

