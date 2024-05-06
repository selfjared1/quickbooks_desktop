import unittest
from lxml import etree
from core.mixins import ToXmlMixin, FromXMLMixin, to_dict

class MockClassWithToXml(ToXmlMixin):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class TestToXmlMixin(unittest.TestCase):
    def test_to_xml_without_custom_tag(self):
        """Test the to_xml method without a custom tag."""
        obj = MockClassWithToXml(attr1="value1", attr2="value2")
        xml_str = obj.to_xml()
        expected_xml_str = "<MockClassWithToXml>\n  <attr1>value1</attr1>\n  <attr2>value2</attr2>\n</MockClassWithToXml>\n"
        self.assertEqual(xml_str, expected_xml_str)

    def test_to_xml_with_custom_tag(self):
        """Test the to_xml method with a custom tag."""
        obj = MockClassWithToXml(attr1="value1", attr2="value2")
        xml_str = obj.to_xml(name_of_start_tag="CustomTag")
        expected_xml_str = "<CustomTag>\n  <attr1>value1</attr1>\n  <attr2>value2</attr2>\n</CustomTag>\n"
        self.assertEqual(xml_str, expected_xml_str)

    def test_to_xml_with_underscore_in_tag(self):
        """Test the to_xml method with an underscore in the custom tag."""
        obj = MockClassWithToXml(attr1="value1", attr2="value2")
        xml_str = obj.to_xml(name_of_start_tag="Custom_Tag")
        expected_xml_str = "<CustomTag>\n  <attr1>value1</attr1>\n  <attr2>value2</attr2>\n</CustomTag>\n"
        self.assertEqual(xml_str, expected_xml_str)

    def test_to_xml_with_skipping_underscores(self):
        """Test the to_xml method to ensure it skips attributes starting with an underscore."""
        obj = MockClassWithToXml(_private_attr="should not be in xml", attr2="value2")
        xml_str = obj.to_xml()
        expected_xml_str = "<MockClassWithToXml>\n  <attr2>value2</attr2>\n</MockClassWithToXml>\n"
        self.assertNotIn("_private_attr", xml_str)
        self.assertIn("<attr2>value2</attr2>", xml_str)

class MockClassWithFromXml(FromXMLMixin):
    class_dict = {
        'SubObject': MockSubClassWithFromXml
    }
    list_dict = {
        'Items': MockListItemWithFromXml
    }

class MockSubClassWithFromXml(FromXMLMixin):
    # This class would have its own from_xml logic, attributes, and methods
    pass

class MockListItemWithFromXml(FromXMLMixin):
    # This class would handle list items from XML
    pass

class TestFromXMLMixin(unittest.TestCase):
    def test_from_xml_with_class_dict(self):
        """Test the from_xml method with a class dictionary."""
        xml_data = '<MockClass><SubObject><Name>TestName</Name></SubObject></MockClass>'
        obj = MockClassWithFromXml.from_xml(xml_data)
        self.assertIsInstance(obj.SubObject, MockSubClassWithFromXml)
        self.assertEqual(obj.SubObject.Name, 'TestName')

    def test_from_xml_with_list_dict(self):
        """Test the from_xml method with a list dictionary."""
        xml_data = '<MockClass><Items><Item><Name>Item1</Name></Item><Item><Name>Item2</Name></Item></Items></MockClass>'
        obj = MockClassWithFromXml.from_xml(xml_data)
        self.assertIsInstance(obj.Items, list)
        self.assertEqual(len(obj.Items), 2)
        self.assertIsInstance(obj.Items[0], MockListItemWithFromXml)
        self.assertEqual(obj.Items[0].Name, 'Item1')
        self.assertEqual(obj.Items[1].Name, 'Item2')

    def test_from_xml_with_simple_attributes(self):
        """Test the from_xml method with simple attributes."""
        xml_data = '<MockClass><Name>Simple Name</Name><Value>123</Value></MockClass>'
        obj = MockClassWithFromXml.from_xml(xml_data)
        self.assertEqual(obj.Name, 'Simple Name')
        self.assertEqual(obj.Value, '123')



class MockClass:
    def __init__(self, value):
        self.value = value
        self._private = 'should not be included'

    def method(self):
        pass  # Methods should not be included in the dictionary

class NestedMockClass:
    def __init__(self):
        self.nested = MockClass(10)

class ComplexIterableMockClass:
    def __init__(self):
        self.iterable = [MockClass(20), MockClass(30)]

class TestToDict(unittest.TestCase):
    def test_to_dict_with_simple_object(self):
        """Test the to_dict function with a simple object."""
        obj = MockClass(1)
        obj_dict = to_dict(obj)
        expected = {'value': 1}
        self.assertEqual(obj_dict, expected)

    def test_to_dict_with_nested_object(self):
        """Test the to_dict function with a nested object."""
        obj = NestedMockClass()
        obj_dict = to_dict(obj)
        expected = {'nested': {'value': 10}}
        self.assertEqual(obj_dict, expected)

    def test_to_dict_with_iterable_object(self):
        """Test the to_dict function with an object containing an iterable."""
        obj = ComplexIterableMockClass()
        obj_dict = to_dict(obj)
        expected = {'iterable': [{'value': 20}, {'value': 30}]}
        self.assertEqual(obj_dict, expected)

    def test_to_dict_with_classkey(self):
        """Test the to_dict function with the classkey argument."""
        obj = MockClass(1)
        obj_dict = to_dict(obj, classkey='classname')
        expected = {'classname': 'MockClass', 'value': 1}
        self.assertEqual(obj_dict, expected)

