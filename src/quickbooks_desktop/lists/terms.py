from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class TermsRef(QBRefMixin):
    class Meta:
        name = "TermsRef"