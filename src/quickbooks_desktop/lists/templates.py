from dataclasses import dataclass
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin

@dataclass
class TemplateRef(QBRefMixin):

    class Meta:
        name = "TemplateRef"

#todo: Templates