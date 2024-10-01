from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from decimal import Decimal
# from src.quickbooks_desktop.lists.employees import Employee as DBEmployee
from src.quickbooks_desktop.qb_contact_common_fields import EmployeeAddress, AdditionalContactRef
from src.quickbooks_desktop.qb_mixin import PluralMixin, QBRefMixin, QBMixin, QBMixinWithQuery, QBQueryMixin
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime
from src.quickbooks_desktop.qb_query_common_fields import NameFilter, NameRangeFilter
from src.quickbooks_desktop.lists.qb_classes import QBClassRef


@dataclass
class EntityRef(QBRefMixin):
    class Meta:
        name = "EntityRef"


def validate_relation(value: Optional[str]) -> Optional[str]:
    VALID_RELATION_VALUES = [
        "Spouse", "Partner", "Mother", "Father", "Sister", "Brother",
        "Son", "Daughter", "Friend", "Other"
    ]
    if value is not None and value not in VALID_RELATION_VALUES:
        raise ValueError(f"Invalid relation: {value}. Must be one of {VALID_RELATION_VALUES}.")
    return value


@dataclass
class EmergencyContact(QBMixin):
    class Meta:
        name = ""

    VALID_RELATION_VALUES = [
        "Spouse", "Partner", "Mother", "Father", "Sister", "Brother",
        "Son", "Daughter", "Friend", "Other"
    ]

    contact_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactName",
            "type": "Element",
            "required": True,
            "max_length": 40,
        },
    )
    contact_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactValue",
            "type": "Element",
            "required": True,
            "max_length": 255,
        },
    )
    relation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Relation",
            "type": "Element",
        },
    )

    def __post_init__(self):
        self._validate_relation(self.relation)

    def _validate_relation(self, value: Optional[str]) -> None:
        if value is not None and value not in self.VALID_RELATION_VALUES:
            raise ValueError(f"Invalid relation: {value}. Must be one of {self.VALID_RELATION_VALUES}.")
        else:
            pass

@dataclass
class PrimaryContact(EmergencyContact):
    class Meta:
        name = "PrimaryContact"

@dataclass
class SecondaryContact(EmergencyContact):
    class Meta:
        name = "SecondaryContact"


@dataclass
class EmergencyContacts(QBMixin):
    class Meta:
        name = "EmergencyContacts"

    primary_contact: Optional[PrimaryContact] = field(
        default=None,
        metadata={
            "name": "PrimaryContact",
            "type": "Element",
        },
    )
    secondary_contact: Optional[SecondaryContact] = field(
        default=None,
        metadata={
            "name": "SecondaryContact",
            "type": "Element",
        },
    )

@dataclass
class SupervisorRef(QBRefMixin):
    class Meta:
        name = "SupervisorRef"


@dataclass
class PayrollItemWageRef(QBRefMixin):
    class Meta:
        name = "PayrollItemWageRef"

@dataclass
class Earnings(QBMixin):
    class Meta:
        name = "Earnings"

    payroll_item_wage_ref: Optional[PayrollItemWageRef] = field(
        default=None,
        metadata={
            "name": "PayrollItemWageRef",
            "type": "Element",
            "required": True,
        },
    )
    rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
        },
    )
    rate_percent: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RatePercent",
            "type": "Element",
        },
    )

@dataclass
class AccruedHours(QBMixin):
    #this class is meant to be inherited
    class Meta:
        name = ""

    hours_available: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursAvailable",
            "type": "Element",
        },
    )
    accrual_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccrualPeriod",
            "type": "Element",
        },
    )
    hours_accrued: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursAccrued",
            "type": "Element",
        },
    )
    maximum_hours: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "MaximumHours",
            "type": "Element",
        },
    )
    is_resetting_hours_each_new_year: Optional[bool] = (
        field(
            default=None,
            metadata={
                "name": "IsResettingHoursEachNewYear",
                "type": "Element",
            },
        )
    )
    hours_used: Optional[QBTime] = field(
        default=None,
        metadata={
            "name": "HoursUsed",
            "type": "Element",
        },
    )
    accrual_start_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AccrualStartDate",
            "type": "Element",
        },
    )

    VALID_ACCRUAL_PERIOD_VALUES = ["BeginningOfYear", "EveryHourOnPaycheck", "EveryPaycheck"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('accrual_period', self.accrual_period, self.VALID_ACCRUAL_PERIOD_VALUES)

@dataclass
class SickHours(AccruedHours):
    #this class is meant to be inherited
    class Meta:
        name = "SickHours"

    employee_payroll_info_id: Optional[int] = None


@dataclass
class VacationHours(AccruedHours):
    #this class is meant to be inherited
    class Meta:
        name = "VacationHours"

    employee_payroll_info_id: Optional[int] = None

@dataclass
class EmployeePayrollInfo(QBMixin):

    class Meta:
        name = "EmployeePayrollInfo"

    pay_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "PayPeriod",
            "type": "Element",
        },
    )
    class_ref: Optional[QBClassRef] = field(
        default=None,
        metadata={
            "name": "ClassRef",
            "type": "Element",
        },
    )
    clear_earnings: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ClearEarnings",
            "type": "Element",
        },
    )
    earnings: List[Earnings] = field(
        default_factory=list,
        metadata={
            "name": "Earnings",
            "type": "Element",
        },
    )
    use_time_data_to_create_paychecks: Optional[str] = field(
        default=None,
        metadata={
            "name": "UseTimeDataToCreatePaychecks",
            "type": "Element",
        },
    )
    sick_hours: Optional[SickHours] = field(
        default=None,
        metadata={
            "name": "SickHours",
            "type": "Element",
        },
    )
    vacation_hours: Optional[VacationHours] = field(
        default=None,
        metadata={
            "name": "VacationHours",
            "type": "Element",
        },
    )

    VALID_PAY_PERIOD_VALUES = ["Daily", "Weekly", "Biweekly", "Semimonthly", "Monthly", "Quarterly", "Yearly"]
    VALID_USE_TIME_DATA_TO_CREATE_PAYCHECKS_VALUES = ["NotSet", "UseTimeData", "DoNotUseTimeData"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('pay_period', self.pay_period,
                                               self.VALID_PAY_PERIOD_VALUES)
        self._validate_str_from_list_of_values('use_time_data_to_create_paychecks', self.use_time_data_to_create_paychecks,
                                               self.VALID_USE_TIME_DATA_TO_CREATE_PAYCHECKS_VALUES)


@dataclass
class BillingRateRef(QBRefMixin):

    class Meta:
        name = "BillingRateRef"

@dataclass
class BillingRate(QBMixin):
    class Meta:
        name = "BillingRate"

    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 31,
        },
    )
    billing_rate_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "BillingRateType",
            "type": "Element",
        },
    )
    #todo: Add Field
    # fixed_billing_rate: Optional[FixedBillingRate] = field(
    #     default=None,
    #     metadata={
    #         "name": "FixedBillingRate",
    #         "type": "Element",
    #     },
    # )
    # billing_rate_per_item_ret: List[BillingRatePerItemRet] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "BillingRatePerItemRet",
    #         "type": "Element",
    #     },
    # )

    VALID_BILLING_RATE_TYPES = ["FixedRate", "PerItem"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('billing_rate_type', self.billing_rate_type, self.VALID_BILLING_RATE_TYPES)


@dataclass
class EmployeeQuery(QBQueryMixin):
    class Meta:
        name = "EmployeeQuery"

    list_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    full_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FullName",
            "type": "Element",
        },
    )
    max_returned: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxReturned",
            "type": "Element",
        },
    )
    active_status: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ActiveStatus",
            "type": "Element",
        },
    )
    from_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "FromModifiedDate",
            "type": "Element",
        },
    )
    to_modified_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ToModifiedDate",
            "type": "Element",
        },
    )
    name_filter: Optional[NameFilter] = field(
        default=None,
        metadata={
            "name": "NameFilter",
            "type": "Element",
        },
    )
    name_range_filter: Optional[NameRangeFilter] = field(
        default=None,
        metadata={
            "name": "NameRangeFilter",
            "type": "Element",
        },
    )
    include_ret_element: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncludeRetElement",
            "type": "Element",
            "max_length": 50,
        },
    )
    owner_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    # meta_data: Optional[str] = field(
    #     default='NoMetaData',
    #     metadata={
    #         "name": "metaData",
    #         "type": "Attribute",
    #     },
    # )
    #
    # VALID_META_DATA_VALUES = ["NoMetaData", "MetaDataOnly", "MetaDataAndResponseData"]
    #
    # def __post_init__(self):
    #     self._validate_str_from_list_of_values('meta_data', self.meta_data, self.VALID_META_DATA_VALUES)

    department_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Department Code",
            "type": "Element",
            "max_length": 99
        },
    )


@dataclass
class Employee(QBMixinWithQuery):
    class Meta:
        name = "Employee"

    class Query(EmployeeQuery):
        pass


    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ListID",
            "type": "Element",
        },
    )
    time_created: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeCreated",
            "type": "Element",
        },
    )
    time_modified: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "TimeModified",
            "type": "Element",
        },
    )
    edit_sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "EditSequence",
            "type": "Element",
            "max_length": 16,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 41,
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "max_length": 15,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "max_length": 25,
        },
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleName",
            "type": "Element",
            "max_length": 5,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "max_length": 25,
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
        },
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobTitle",
            "type": "Element",
            "max_length": 41,
        },
    )
    supervisor_ref: Optional[SupervisorRef] = field(
        default=None,
        metadata={
            "name": "SupervisorRef",
            "type": "Element",
        },
    )
    department: Optional[str] = field(
        default=None,
        metadata={
            "name": "Department",
            "type": "Element",
            "max_length": 31,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "max_length": 64,
        },
    )
    target_bonus: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TargetBonus",
            "type": "Element",
        },
    )
    employee_address: Optional[EmployeeAddress] = field(
        default=None,
        metadata={
            "name": "EmployeeAddress",
            "type": "Element",
        },
    )
    print_as: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrintAs",
            "type": "Element",
            "max_length": 41,
        },
    )
    phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phone",
            "type": "Element",
            "max_length": 21,
        },
    )
    mobile: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mobile",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pager",
            "type": "Element",
            "max_length": 21,
        },
    )
    pager_pin: Optional[str] = field(
        default=None,
        metadata={
            "name": "PagerPIN",
            "type": "Element",
            "max_length": 10,
        },
    )
    alt_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "AltPhone",
            "type": "Element",
            "max_length": 21,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "max_length": 21,
        },
    )
    ssn: Optional[str] = field(
        default=None,
        metadata={
            "name": "SSN",
            "type": "Element",
            "max_length": 11,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "max_length": 1023,
        },
    )
    # additional_contact_ref: List[AdditionalContactRef] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "AdditionalContactRef",
    #         "type": "Element",
    #         "max_occurs": 8,
    #     },
    # )
    emergency_contacts: Optional[EmergencyContacts] = field(
        default=None,
        metadata={
            "name": "EmergencyContacts",
            "type": "Element",
        },
    )
    employee_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "EmployeeType",
            "type": "Element",
        },
    )
    part_or_full_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartOrFullTime",
            "type": "Element",
        },
    )
    exempt: Optional[str] = field(
        default=None,
        metadata={
            "name": "Exempt",
            "type": "Element",
        },
    )
    key_employee: Optional[bool] = field(
        default=None,
        metadata={
            "name": "KeyEmployee",
            "type": "Element",
        },
    )
    gender: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
        },
    )
    hired_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "HiredDate",
            "type": "Element",
        },
    )
    original_hire_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "OriginalHireDate",
            "type": "Element",
        },
    )
    adjusted_service_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "AdjustedServiceDate",
            "type": "Element",
        },
    )
    released_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "ReleasedDate",
            "type": "Element",
        },
    )
    birth_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
        },
    )
    us_citizen: Optional[bool] = field(
        default=None,
        metadata={
            "name": "USCitizen",
            "type": "Element",
        },
    )
    ethnicity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ethnicity",
            "type": "Element",
        },
    )
    disabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Disabled",
            "type": "Element",
        },
    )
    disability_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "DisabilityDesc",
            "type": "Element",
            "max_length": 25,
        },
    )
    on_file: Optional[bool] = field(
        default=None,
        metadata={
            "name": "OnFile",
            "type": "Element",
        },
    )
    work_auth_expire_date: Optional[QBDates] = field(
        default=None,
        metadata={
            "name": "WorkAuthExpireDate",
            "type": "Element",
        },
    )
    us_veteran: Optional[bool] = field(
        default=None,
        metadata={
            "name": "USVeteran",
            "type": "Element",
        },
    )
    military_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "MilitaryStatus",
            "type": "Element",
        },
    )
    account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "max_length": 99,
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "max_length": 4095,
        },
    )
    # additional_notes_ret: List[AdditionalNotes] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "AdditionalNotesRet",
    #         "type": "Element",
    #     },
    # )
    billing_rate_ref: Optional[BillingRateRef] = field(
        default=None,
        metadata={
            "name": "BillingRateRef",
            "type": "Element",
        },
    )
    employee_payroll_info: Optional[EmployeePayrollInfo] = field(
        default=None,
        metadata={
            "name": "EmployeePayrollInfo",
            "type": "Element",
        },
    )
    #todo: Add Field
    # external_guid: Optional[ExternalGuid] = field(
    #     default=None,
    #     metadata={
    #         "name": "ExternalGUID",
    #         "type": "Element",
    #     },
    # )
    # data_ext_ret: List[DataExtRet] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "DataExtRet",
    #         "type": "Element",
    #     },
    # )

    IS_YES_NO_FIELD_LIST = ["key_employee", "us_citizen", "disabled", "on_file", "us_veteran"]
    VALID_EMPLOYEE_TYPES = ["Officer", "Owner", "Regular", "Statutory"]
    VALID_PART_OR_FULL_TIME_VALUES = ["PartTime", "FullTime"]
    VALID_EXEMPT_VALUES = ["Exempt", "NonExempt"]
    VALID_GENDER_VALUES = ["Male", "Female"]
    VALID_ETHNICITY_VALUES = ["AmericianIndian", "Asian", "Black", "Hawaiian", "Hispanic", "White", "TwoOrMoreRaces"]
    VALID_MILITARY_STATUS_VALUES = ["Active", "Reserve"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('employee_type', self.employee_type, self.VALID_EMPLOYEE_TYPES)
        self._validate_str_from_list_of_values('part_or_full_time', self.part_or_full_time, self.VALID_PART_OR_FULL_TIME_VALUES)
        self._validate_str_from_list_of_values('exempt', self.exempt, self.VALID_EXEMPT_VALUES)
        self._validate_str_from_list_of_values('gender', self.gender, self.VALID_GENDER_VALUES)
        self._validate_str_from_list_of_values('ethnicity', self.ethnicity, self.VALID_ETHNICITY_VALUES)
        self._validate_str_from_list_of_values('military_status', self.military_status, self.VALID_MILITARY_STATUS_VALUES)

class Employees(PluralMixin):

    class Meta:
        name = "Employee"
        plural_of = Employee
        plural_of_db_model = DBEmployee
