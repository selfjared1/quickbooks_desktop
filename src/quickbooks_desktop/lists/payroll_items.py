from dataclasses import dataclass, field
from typing import Optional
from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.qb_mixin import QBMixin
from src.quickbooks_desktop.lists.accounts import ExpenseAccountRef
from src.quickbooks_desktop.qb_mixin import QBRefMixin

@dataclass
class PayrollItemWageRef(QBRefMixin):
    class Meta:
        name = "PayrollItemWage"

@dataclass
class PayrollItemWage(QBMixin):


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
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
        },
    )
    wage_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "WageType",
            "type": "Element",
        },
    )
    expense_account_ref: Optional[ExpenseAccountRef] = field(
        default=None,
        metadata={
            "name": "ExpenseAccountRef",
            "type": "Element",
        },
    )

    VALID_WAGE_TYPE_VALUES = ["Bonus", "Commission", "HourlyOvertime", "HourlyRegular", "HourlySick",
                              "HourlyVacation", "SalaryRegular", "SalarySick", "SalaryVacation"]

    def __post_init__(self):
        self._validate_str_from_list_of_values('wage_type', self.wage_type, self.VALID_WAGE_TYPE_VALUES)