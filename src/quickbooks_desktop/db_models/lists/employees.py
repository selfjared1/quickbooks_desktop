from sqlalchemy import Column, String, Boolean, Integer, DECIMAL, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.quickbooks_desktop.db_models.base import Base
from src.quickbooks_desktop.db_models.db_models_mixins import PluralMixin
from src.quickbooks_desktop.common.qb_contact_common import AdditionalContactRef

class Employee(Base):
    __tablename__ = 'qb_employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=True)
    time_modified = Column(DateTime, nullable=True)
    edit_sequence = Column(String(16), nullable=True)
    name = Column(String(41), nullable=True)
    is_active = Column(Boolean, nullable=True)
    salutation = Column(String(15), nullable=True)
    first_name = Column(String(25), nullable=True)
    middle_name = Column(String(5), nullable=True)
    last_name = Column(String(25), nullable=True)
    suffix = Column(String, nullable=True)
    job_title = Column(String(41), nullable=True)
    supervisor_ref_list_id = Column(Text, nullable=True)
    supervisor_ref_full_name = Column(Text, nullable=True)
    department = Column(String(31), nullable=True)
    description = Column(String(64), nullable=True)
    target_bonus = Column(DECIMAL, nullable=True)
    print_as = Column(String(41), nullable=True)
    phone = Column(String(21), nullable=True)
    mobile = Column(String(21), nullable=True)
    pager = Column(String(21), nullable=True)
    pager_pin = Column(String(10), nullable=True)
    alt_phone = Column(String(21), nullable=True)
    fax = Column(String(21), nullable=True)
    ssn = Column(String(11), nullable=True)
    email = Column(String(1023), nullable=True)
    employee_type = Column(String, nullable=True)
    part_or_full_time = Column(String, nullable=True)
    exempt = Column(String, nullable=True)
    key_employee = Column(Boolean, nullable=True)
    gender = Column(String, nullable=True)
    hired_date = Column(DateTime, nullable=True)
    original_hire_date = Column(DateTime, nullable=True)
    adjusted_service_date = Column(DateTime, nullable=True)
    released_date = Column(DateTime, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    us_citizen = Column(Boolean, nullable=True)
    ethnicity = Column(String, nullable=True)
    disabled = Column(Boolean, nullable=True)
    disability_desc = Column(String(25), nullable=True)
    on_file = Column(Boolean, nullable=True)
    work_auth_expire_date = Column(DateTime, nullable=True)
    us_veteran = Column(Boolean, nullable=True)
    military_status = Column(String, nullable=True)
    account_number = Column(String(99), nullable=True)
    notes = Column(String(4095), nullable=True)
    department_code = Column(String(99), nullable=True)

    billing_rate_ref_id = Column(Integer, ForeignKey('billing_rates.id'), nullable=True)

    addresses = relationship('Address', back_populates='employee', cascade="all, delete-orphan")
    additional_contact_ref = relationship('AdditionalContactRef', back_populates='employee', foreign_keys=[AdditionalContactRef.employee_id], cascade="all, delete-orphan")

    employee_payroll_info = relationship('EmployeePayrollInfo', uselist=False, back_populates='employee', cascade="all, delete-orphan")

    department_code_dict = {
        500: "Consulting",
        600: "Rehab",
        700: "Finance & Accounting",
        800: "Clinical",
        1100: "Healthcare",
        1200: "Business Profession"
    }

    @classmethod
    def get_from_kaiser_report_time_entry(cls, kaiser_report_time_entry, session):
        match = session.query(Employee).filter_by(name=kaiser_report_time_entry.worker).all()
        if len(match) == 1:
            employee = match[0]
            return employee
        else:
            last_name = kaiser_report_time_entry.worker.split(',')[0]
            match = session.query(Employee).filter_by(last_name=last_name).all()
            if len(match) == 1:
                employee = match[0]
                return employee
            else:
                match = session.query(Employee).filter_by(email=kaiser_report_time_entry.email).all()
                if len(match) == 1:
                    employee = match[0]
                    return employee
                else:
                    return None


class EmployeePayrollInfo(Base):
    __tablename__ = 'employee_payroll_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pay_period = Column(String, nullable=True)
    class_ref_list_id = Column(Text, nullable=True)
    class_ref_full_name = Column(Text, nullable=True)
    clear_earnings = Column(Boolean, nullable=True)
    use_time_data_to_create_paychecks = Column(String, nullable=True)
    earnings = relationship('Earnings', back_populates='employee_payroll_info', cascade="all, delete-orphan")

    employee_id = Column(Integer, ForeignKey('qb_employees.id', ondelete='CASCADE'), nullable=False)
    employee = relationship('Employee', back_populates='employee_payroll_info')

    sick_hours = relationship('SickHours', uselist=False, back_populates='employee_payroll_info', cascade="all, delete-orphan")
    vacation_hours = relationship('VacationHours', uselist=False, back_populates='employee_payroll_info', cascade="all, delete-orphan")


class AccruedHours(Base):
    __tablename__ = 'accrued_hours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hours_available = Column(DECIMAL, nullable=True)
    accrual_period = Column(String, nullable=True)
    hours_accrued = Column(DECIMAL, nullable=True)
    maximum_hours = Column(DECIMAL, nullable=True)
    is_resetting_hours_each_new_year = Column(Boolean, nullable=True)
    hours_used = Column(DECIMAL, nullable=True)
    accrual_start_date = Column(DateTime, nullable=True)


class SickHours(AccruedHours):
    __tablename__ = 'sick_hours'

    id = Column(Integer, ForeignKey('accrued_hours.id'), primary_key=True)
    employee_payroll_info_id = Column(Integer, ForeignKey('employee_payroll_info.id', ondelete='CASCADE'), nullable=False)
    employee_payroll_info = relationship('EmployeePayrollInfo', back_populates='sick_hours')


class VacationHours(AccruedHours):
    __tablename__ = 'vacation_hours'

    id = Column(Integer, ForeignKey('accrued_hours.id'), primary_key=True)
    employee_payroll_info_id = Column(Integer, ForeignKey('employee_payroll_info.id', ondelete='CASCADE'), nullable=False)
    employee_payroll_info = relationship('EmployeePayrollInfo', back_populates='vacation_hours')


class Earnings(Base):
    __tablename__ = 'earnings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_item_wage_ref_list_id = Column(Text, nullable=True)
    payroll_item_wage_ref_full_name = Column(Text, nullable=True)
    rate = Column(DECIMAL, nullable=True)
    rate_percent = Column(DECIMAL, nullable=True)
    employee_payroll_info_id = Column(Integer, ForeignKey('employee_payroll_info.id'), nullable=False)
    employee_payroll_info = relationship('EmployeePayrollInfo', back_populates='earnings')

class BillingRate(Base):
    __tablename__ = 'billing_rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=True)
    time_modified = Column(DateTime, nullable=True)
    edit_sequence = Column(String(16), nullable=True)
    name = Column(String(31), nullable=True)
    billing_rate_type = Column(String, nullable=True)


class Employees(PluralMixin, PluralListSaveMixin):
    class Meta:
        name = "employees"
        plural_of_db_model = Employee

    @classmethod
    def get_by_name(cls, name, session):
        # Query the database to find an employee with a matching name
        employee = session.query(Employee).filter(Employee.name == name).first()
        return employee