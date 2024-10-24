from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin
from dataclasses import dataclass

@dataclass
class PrefVendorRef(QBRefMixin):
    class Meta:
        name = "PrefVendorRef"