from dataclasses import dataclass
from src.quickbooks_desktop.qb_mixin import QBRefMixin

@dataclass
class TermsRef(QBRefMixin):
    class Meta:
        name = "TermsRef"