from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.quickbooks_desktop.db_models.base import Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address_type = Column(String, nullable=False)  # To specify the type of address
    addr1 = Column(String, nullable=True)
    addr2 = Column(String, nullable=True)
    addr3 = Column(String, nullable=True)
    addr4 = Column(String, nullable=True)
    addr5 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    note = Column(String, nullable=True)
    customer_id = Column(Integer, ForeignKey('qb_customers.id'), nullable=True)
    customer = relationship("Customer", back_populates="addresses")
    employee_id = Column(Integer, ForeignKey('qb_employees.id'), nullable=True)
    employee = relationship("Employee", back_populates="addresses")

class AdditionalContactRef(Base):
    __tablename__ = 'additional_contact_ref'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_name = Column(String(40), nullable=False)
    contact_value = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey('qb_customers.id'))
    customer = relationship("Customer", back_populates="additional_contact_ref", foreign_keys=[customer_id])
    employee_id = Column(Integer, ForeignKey('qb_employees.id'))
    employee = relationship("Employee", back_populates="additional_contact_ref", foreign_keys=[employee_id])


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=False)
    time_modified = Column(DateTime, nullable=False)
    edit_sequence = Column(String(16), nullable=True)
    contact = Column(String(41), nullable=True)
    salutation = Column(String(15), nullable=True)
    first_name = Column(String(25), nullable=False)
    middle_name = Column(String(5), nullable=True)
    last_name = Column(String(25), nullable=True)
    job_title = Column(String(41), nullable=True)

    customer_id = Column(Integer, ForeignKey('qb_customers.id'))
    customer = relationship("Customer", back_populates="contacts_rets", foreign_keys=[customer_id])


