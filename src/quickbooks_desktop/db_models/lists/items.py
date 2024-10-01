from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.quickbooks_desktop.db_models.base import Base
from src.quickbooks_desktop.db_models.db_models_mixins import PluralMixin

class ItemService(Base):
    __tablename__ = 'qb_item_service'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=True)
    time_modified = Column(DateTime, nullable=True)
    edit_sequence = Column(String(16), nullable=True)
    name = Column(String(31), nullable=True)
    full_name = Column(String(159), nullable=True)
    bar_code_value = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=True)
    sublevel = Column(Integer, nullable=True)
    is_tax_included = Column(Boolean, nullable=True)

    class_ref_list_id = Column(Text, nullable=True)
    class_ref_full_name = Column(Text, nullable=True)
    parent_ref_list_id = Column(Text, nullable=True)
    parent_ref_full_name = Column(Text, nullable=True)
    unit_of_measure_set_ref_list_id = Column(Text, nullable=True)
    unit_of_measure_set_ref_full_name = Column(Text, nullable=True)
    sales_tax_code_ref_list_id = Column(Text, nullable=True)
    sales_tax_code_ref_full_name = Column(Text, nullable=True)

    sales_or_purchase_desc = Column(Text, nullable=True)
    sales_or_purchase_price = Column(Text, nullable=True)
    sales_or_purchase_price_percent = Column(Text, nullable=True)
    sales_or_purchase_account_ref_list_id = Column(Text, nullable=True)
    sales_or_purchase_account_ref_full_name = Column(Text, nullable=True)

    sales_and_purchase_sales_desc = Column(Text, nullable=True)
    sales_and_purchase_sales_price = Column(Text, nullable=True)
    sales_and_purchase_income_account_ref_list_id = Column(Text, nullable=True)
    sales_and_purchase_income_account_ref_full_name = Column(Text, nullable=True)
    sales_and_purchase_purchase_desc = Column(Text, nullable=True)
    sales_and_purchase_purchase_cost = Column(Text, nullable=True)
    sales_and_purchase_purchase_tax_code_ref_list_id = Column(Text, nullable=True)
    sales_and_purchase_purchase_tax_code_ref_full_name = Column(Text, nullable=True)
    sales_and_purchase_expense_account_ref_list_id = Column(Text, nullable=True)
    sales_and_purchase_expense_account_ref_full_name = Column(Text, nullable=True)
    sales_and_purchase_pref_vendor_ref_list_id = Column(Text, nullable=True)
    sales_and_purchase_pref_vendor_ref_full_name = Column(Text, nullable=True)

    qb_id_tracker_id = Column(Integer, ForeignKey('qb_id_tracker.id'), nullable=True)
    qb_id_tracker = relationship('QBIDTracker', back_populates='qb_item_service')


class ItemServices(PluralMixin):
    class Meta:
        name = "qb_item_service"
        plural_of_db_model = ItemService