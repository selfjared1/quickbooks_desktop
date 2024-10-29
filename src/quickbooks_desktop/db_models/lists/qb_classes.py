from sqlalchemy import Column, String, Boolean, Integer, DateTime
from src.quickbooks_desktop.db_models.db_models_mixins import PluralMixin
from src.quickbooks_desktop.db_models.base import Base


class DBofQBClass(Base):
    __tablename__ = 'qb_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String)
    time_created = Column(DateTime)
    time_modified = Column(DateTime)
    edit_sequence = Column(String(16))
    name = Column(String(31))
    full_name = Column(String(159))
    is_active = Column(Boolean)
    parent_ref = Column(String)
    sublevel = Column(Integer)

class DBofQBClasses(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "qb_class"
        plural_of_db_model = DBofQBClass