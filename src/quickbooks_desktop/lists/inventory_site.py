from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class InventorySiteRef(QBRefMixin):

    class Meta:
        name = "InventorySiteRef"

@dataclass
class InventorySiteLocationRef(QBRefMixin):

    class Meta:
        name = "InventorySiteLocationRef"