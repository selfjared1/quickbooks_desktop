from lxml import etree
from core.special_fields import QBDates

class QBMetaData:
    qb_dates_dict = {}
    def __init__(self):
        self.TimeCreated = QBDates('')
        self.TimeModified = QBDates('')
        self.EditSequence = ""

class FromXMLMixin:
    ref_dict = {}
    list_dict = {}

    def from_xml(self, xml_data):
        tree = etree.fromstring(xml_data)
        for ref_name, field_name in self.ref_dict.items():
            element = tree.find(ref_name)
            if element is not None:
                setattr(self, field_name, element.text)

        for list_name, list_field_name in self.list_dict.items():
            elements = tree.findall(list_name)
            if elements:
                setattr(self, list_field_name, [elem.text for elem in elements])



class ValidateMaxLengthMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._attributes = {}

    def _check_max_length(self, value, max_length):
        if value and len(value) > max_length:
            raise ValueError(f"Value exceeds maximum length of {max_length} characters")
        return value

    @classmethod
    def add_validated_property(cls, attribute, max_length):
        private_name = f"_{attribute}"

        def getter(self):
            return getattr(self, private_name, None)

        def setter(self, value):
            validated_value = self._check_max_length(value, max_length)
            setattr(self, private_name, validated_value)

        setattr(cls, attribute, property(getter, setter))

class QBDesktopObjectBaseMixin(QBMetaData, FromXMLMixin, ValidateMaxLengthMixin):

    def __init__(self):
        super(QBDesktopObjectBaseMixin, self).__init__()





