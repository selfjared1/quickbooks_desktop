from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class PriceLevelRef(QBRefMixin):

    class Meta:
        name = "PriceLevelRef"

#todo: Templates