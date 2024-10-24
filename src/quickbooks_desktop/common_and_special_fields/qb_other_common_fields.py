from dataclasses import dataclass

from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin


@dataclass
class ParentRef(QBRefMixin):

    class Meta:
        name = "ParentRef"
