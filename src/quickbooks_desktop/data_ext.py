
from src.quickbooks_desktop.mixins.qb_mixins import QBRefMixin, QBMixinWithQuery, QBMixin, QBQueryMixin, QBAddMixin, QBModMixin, ListSaveMixin
from src.quickbooks_desktop.mixins.qb_plural_mixins import PluralListSaveMixin


@dataclass
class DataExt(QBMixinWithQuery, ListSaveMixin):

    class Meta:
        name = "Account"

    Query: Type[AccountQuery] = AccountQuery
    Add: Type[AccountAdd] = AccountAdd
    Mod: Type[AccountMod] = AccountMod

    owner_id: Optional[OwnerId] = field(
        default=None,
        metadata={
            "name": "OwnerID",
            "type": "Element",
        },
    )
    data_ext_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataExtName",
            "type": "Element",
            "required": True,
            "max_length": 31,
        },
    )
    data_ext_type: Optional[DataExtType] = field(
        default=None,
        metadata={
            "name": "DataExtType",
            "type": "Element",
            "required": True,
        },
    )
    data_ext_value: Optional[DataExtValue] = field(
        default=None,
        metadata={
            "name": "DataExtValue",
            "type": "Element",
            "required": True,
        },
    )