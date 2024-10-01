from src.quickbooks_desktop.qb_mixin import QBRefMixin
from dataclasses import dataclass

@dataclass
class PrefVendorRef(QBRefMixin):
    class Meta:
        name = "PrefVendorRef"