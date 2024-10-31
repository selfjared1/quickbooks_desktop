from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Type, Dict
from collections import defaultdict
from src.quickbooks_desktop.data_ext import DataExt
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.common import (
    LinkedTxn, BillAddress, BillAddressBlock, ShipAddress, ShipAddressBlock, SetCredit,
    ModifiedDateRangeFilter, TxnDateRangeFilter, EntityFilter, AccountFilter, RefNumberFilter, RefNumberRangeFilter,
    CurrencyFilter, LinkToTxn
)
from src.quickbooks_desktop.lists import (
    SalesTaxCodeRef, ItemSalesTaxRef, TemplateRef, CustomerRef, ClassInQBRef, AraccountRef, CurrencyRef, TermsRef,
    SalesRepRef, ShipMethodRef, CustomerMsgRef, CustomerSalesTaxCodeRef, ItemRef, OverrideUomsetRef, InventorySiteRef,
    InventorySiteLocationRef, ItemGroupRef, PriceLevelRef, OverrideItemAccountRef, AccountRef
)
from src.quickbooks_desktop.mixins import (
    PluralMixin, PluralTrxnSaveMixin, QBRefMixin, QBMixinWithQuery, QBMixin,
    QBQueryMixin, QBAddMixin, QBModMixin, SaveMixin
)
