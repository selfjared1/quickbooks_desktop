from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class ShipMethodRef(QBRefMixin):

    class Meta:
        name = "ShipMethodRef"