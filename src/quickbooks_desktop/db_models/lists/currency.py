from sqlalchemy import Column, String, Boolean, Integer, DECIMAL, DateTime
from src.quickbooks_desktop.db_models.base import Base
from src.quickbooks_desktop.db_models.db_models_mixins import PluralMixin

class DBCurrency(Base):
    __tablename__ = 'qb_currency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=True)
    time_modified = Column(DateTime, nullable=True)
    edit_sequence = Column(String(16), nullable=True)
    name = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=True)
    currency_code = Column(String(3), nullable=True)
    currency_format = Column(String, nullable=True)  # Assuming this is a string field, adjust if needed
    is_user_defined_currency = Column(Boolean, nullable=True)
    exchange_rate = Column(DECIMAL, nullable=True)
    as_of_date = Column(DateTime, nullable=True)  # Assuming QBDates is compatible with DateTime, adjust if necessary

class DBCurrencies(PluralMixin):
    class Meta:
        name = "qb_currency"
        plural_of_db_model = DBCurrency
