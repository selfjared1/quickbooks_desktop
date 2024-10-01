from dataclasses import dataclass

from src.quickbooks_desktop.qb_mixin import QBRefMixin


@dataclass
class ParentRef(QBRefMixin):

    class Meta:
        name = "ParentRef"
