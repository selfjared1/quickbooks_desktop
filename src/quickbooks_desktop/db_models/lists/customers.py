from sqlalchemy import Column, String, Boolean, Integer, DECIMAL, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.quickbooks_desktop.qb_contact_common_fields import AdditionalContactRef, Contacts
from src.quickbooks_desktop.db_models.base import Base
from src.quickbooks_desktop.db_models.db_models_mixins import PluralMixin

class Customer(Base):
    __tablename__ = 'qb_customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, unique=True, nullable=True)
    time_created = Column(DateTime, nullable=True)
    time_modified = Column(DateTime, nullable=True)
    edit_sequence = Column(String(16), nullable=True)
    name = Column(String(41), nullable=True)
    full_name = Column(String(209), nullable=True)
    is_active = Column(Boolean, nullable=True)
    sublevel = Column(Integer, nullable=True)
    company_name = Column(String(41), nullable=True)
    salutation = Column(String(15), nullable=True)
    first_name = Column(String(25), nullable=True)
    middle_name = Column(String(5), nullable=True)
    last_name = Column(String(25), nullable=True)
    suffix = Column(String, nullable=True)
    job_title = Column(String(41), nullable=True)
    print_as = Column(String(41), nullable=True)
    phone = Column(String(21), nullable=True)
    mobile = Column(String(21), nullable=True)
    pager = Column(String(21), nullable=True)
    alt_phone = Column(String(21), nullable=True)
    fax = Column(String(21), nullable=True)
    email = Column(String(1023), nullable=True)
    cc = Column(String(1023), nullable=True)
    contact = Column(String(41), nullable=True)
    alt_contact = Column(String(41), nullable=True)
    balance = Column(DECIMAL, nullable=True)
    total_balance = Column(DECIMAL, nullable=True)
    resale_number = Column(String(15), nullable=True)
    account_number = Column(String(99), nullable=True)
    credit_limit = Column(String, nullable=True)
    job_start_date = Column(DateTime, nullable=True)
    job_projected_end_date = Column(DateTime, nullable=True)
    job_end_date = Column(DateTime, nullable=True)
    job_desc = Column(String(99), nullable=True)
    notes = Column(Text, nullable=True)
    is_statement_with_parent = Column(Boolean, nullable=True)

    # Define relationships for nested elements
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    additional_contact_ref = relationship("AdditionalContactRef", back_populates="customer", foreign_keys=[AdditionalContactRef.customer_id], cascade="all, delete-orphan")
    contacts_rets = relationship("Contacts", back_populates="customer", foreign_keys=[Contacts.customer_id], cascade="all, delete-orphan")

    class_ref_list_id = Column(Text, nullable=True)
    class_ref_full_name = Column(Text, nullable=True)

    parent_ref_list_id = Column(Text, nullable=True)
    parent_ref_full_name = Column(Text, nullable=True)

    customer_type_ref_list_id = Column(Text, nullable=True)
    customer_type_ref_full_name = Column(Text, nullable=True)

    terms_ref_list_id = Column(Text, nullable=True)
    terms_ref_full_name = Column(Text, nullable=True)

    sales_rep_ref_list_id = Column(Text, nullable=True)
    sales_rep_ref_full_name = Column(Text, nullable=True)


class Customers(PluralMixin):
    class Meta:
        name = "customers"
        plural_of_db_model = Customer

    @classmethod
    def get_by_list_id(cls, session, list_id):
        # Query the database for a customer with an exact list_id match
        matching_customer = session.query(Customer).filter(Customer.list_id == list_id).first()
        return matching_customer

    @classmethod
    def get_by_name(cls, session, name):
        # Query the database for a customer with an exact name match
        matching_customers = session.query(Customer).filter(Customer.name == name).first()
        customers = cls()
        customers.add_items(matching_customers)
        return customers