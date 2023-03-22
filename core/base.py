from datetime import datetime
from typing import Optional
from core.special_fields import DataExtRet

class QBObjectBaseMixin:
    def __getattr__(self, name):
        try:
            return getattr(self.qb_object_base, name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if hasattr(self, 'qb_object_base') and hasattr(self.qb_object_base, name):
            setattr(self.qb_object_base, name, value)
        else:
            super().__setattr__(name, value)

class QBBase:
    def __init__(self,
                 list_id: Optional[str] = None,
                 time_created: Optional[datetime] = None,
                 time_modified: Optional[datetime] = None,
                 edit_sequence: Optional[str] = None,
                 data_ext_ret: Optional[DataExtRet] = None,
                 ):
        self.list_id = list_id
        self.time_created = time_created
        self.time_modified = time_modified
        self.edit_sequence = edit_sequence
        self.data_ext_ret = data_ext_ret

class QBListBase(QBObjectBaseMixin):
    def __init__(self,
                 name: Optional[str] = None,
                 full_name: Optional[str] = None,
                 is_active: Optional[bool] = None,
                 desc: Optional[str] = None,
                 parent_ref_list_id: Optional[str] = None,
                 parent_ref_full_name: Optional[str] = None,
                 sublevel: Optional[int] = None,
                 **kwargs,
                 ):
        super().__init__(
            list_id=None,
            time_created=None,
            time_modified=None,
            edit_sequence=None,
            data_ext_ret=None)
        self.qb_base = QBBase(**kwargs)
        self.name = name
        self.full_name = full_name
        self.is_active = is_active
        self.desc = desc
        self.parent_ref_list_id = parent_ref_list_id
        self.parent_ref_full_name = parent_ref_full_name
        self.sublevel = sublevel

class QBTransactionBase(QBObjectBaseMixin):
    """" Multi currency is not supported yet"""
    def __init__(self,
                 txn_id: Optional[str] = None,
                 txn_number: Optional[str] = None,
                 ref_number: Optional[str] = None,
                 memo: Optional[str] = None,
                 external_guid: Optional[str] = None,
                 linked_txns: Optional[list] = None,
                 **kwargs
                 ):
        super().__init__(
            list_id=None,
            time_created=None,
            time_modified=None,
            edit_sequence=None,
            data_ext_ret=None)
        self.qb_base = QBBase(**kwargs)
        self.txn_id = txn_id
        self.txn_number = txn_number
        self.ref_number = ref_number
        self.memo = memo
        self.external_guid = external_guid
        self.linked_txns = linked_txns
