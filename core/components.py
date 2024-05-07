from lxml import etree

class NameFilter:

    def __init__(self):
        self.StartsWith = ''
        self.Contains = ''
        self.EndsWith = ''

    def to_xml(self):
        root = etree.Element("NameFilter")
        if self.StartsWith != '':
            match_criterion_element = etree.SubElement(root, "MatchCriterion")
            match_criterion_element.text = 1
            name_element = etree.SubElement(root, "Name")
            name_element.text = self.StartsWith
        else:
            pass

        if self.Contains != '':
            match_criterion_element = etree.SubElement(root, "MatchCriterion")
            match_criterion_element.text = 2
            name_element = etree.SubElement(root, "Name")
            name_element.text = self.StartsWith
        else:
            pass

        if self.EndsWith != '':
            match_criterion_element = etree.SubElement(root, "MatchCriterion")
            match_criterion_element.text = 3
            name_element = etree.SubElement(root, "Name")
            name_element.text = self.StartsWith
        else:
            pass

        return root

class NameRangeFilter:
    # todo: finish this
    pass

class TotalBalanceFilter:
    def __init__(self):
        self.LessThan = ''
        self.LessThanEqual = ''
        self.Equal = ''
        self.GreaterThan = ''
        self.GreaterThanEqual = ''

    def to_xml(self):
        root = etree.Element("NameRangeFilter")
        def check_value(value):
            if isinstance(value, str):
                if value.isdigit():
                    return float(value)
                elif value == '':
                    return None
            # Todo: check other values

        if self.LessThan != '':
            match_criterion_element = etree.SubElement(root, "Operator")
            match_criterion_element.text = 1
            name_element = etree.SubElement(root, "Amount")
            name_element.text = self.StartsWith
        else:
            pass

        if self.LessThanEqual != '':
            match_criterion_element = etree.SubElement(root, "Operator")
            match_criterion_element.text = 1
            name_element = etree.SubElement(root, "Amount")
            name_element.text = self.StartsWith
        else:
            pass

        if self.LessThan != '':
            match_criterion_element = etree.SubElement(root, "Operator")
            match_criterion_element.text = 1
            name_element = etree.SubElement(root, "Amount")
            name_element.text = self.StartsWith
        else:
            pass

        if self.LessThan != '':
            match_criterion_element = etree.SubElement(root, "Operator")
            match_criterion_element.text = 1
            name_element = etree.SubElement(root, "Amount")
            name_element.text = self.StartsWith
        else:
            pass

        return root