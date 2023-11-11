from lxml import etree

class SaveMixin(object):
    def save(self, ignore_none=True):
        if hasattr(self, 'ListID'):
            if self.ListID is None:
                self.create_list()
            else:
                self.update_list(ignore_none=ignore_none)
        elif hasattr(self, 'TxnID'):
            if self.TxnID is None:
                self.create_txn()
            else:
                self.update_txn(ignore_none=ignore_none)


class GetMixin(object):

    def get(self, qb):
        root = etree.Element(str(self.__class__.__name__) + 'QueryRq')
        for key in self.query_direct_dict:
            if getattr(self, key) is not None:
                #todo: add support for type checks
                #todo: add support for subelements
                root.append(etree.Element(key, str(getattr(self, key))))
            else:
                pass
        xml_data = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
        response = qb.send_xml(xml_data)
        root = etree.fromstring(response)
        response_etree_list = root.findall(str(self.__class__.__name__) + 'Ret')
        if len(response_etree_list) > 0:
            response_list = []
            for element_root in response_etree_list:
                response_list.append(self.from_root(element_root))
            return response_list
        else:
            return []

class ToXmlMixin(object):
    def to_xml(self, request_type=None):
        """
            This mixin is used to convert a QuickBooks Desktop object into an XML string
            request_type can be one of the following depending on the object: 'Query', 'Add', 'Mod'
            To delete requires a different method like "ListDel" or "TxnDel"
            To void use "TxnVoid"
        """
        if request_type is None:
            name_of_start_tag = str(self.__class__.__name__) + 'QueryRq'
        elif request_type[-2:] == 'Rq':
            name_of_start_tag = request_type
            request_type = request_type[:-2]
        else:
            name_of_start_tag = str(self.__class__.__name__) + request_type + 'Rq'
        root = etree.Element(name_of_start_tag)

        for key, value in vars(self).items():
            match type(value):
                case 'str':
                    sub_element = etree.Element(key)
                    sub_element.text = value
                    root.append(sub_element)
                case 'Ref':
                    sub_element = etree.fromstring(value.to_xml())
                    root.append(sub_element)
                case 'QBDate':
                    sub_element = etree.fromstring(value.to_xml())
                    root.append(sub_element)
                case 'list':
                    for item in value:
                        sub_element = etree.fromstring(item.to_xml())
                        root.append(sub_element)
                case 'dict':
                    for key, value in value:
                        sub_element = etree.Element(key)
                        sub_element.text = value
                        root.append(sub_element)


        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
        return xml_str

class FromXMLMixin(object):
    class_dict = {}
    list_dict = {}

    @classmethod
    def from_xml(cls, xml_ret_data):
        root = etree.fromstring(xml_ret_data)
        obj = cls.from_root(root)
        return obj

    @classmethod
    def from_root(cls, root):
        obj = cls()
        print(root.keys())
        for element in root.getchildren():
            if element.tag in obj.class_dict:
                sub_obj = obj.class_dict[element.tag]()
                sub_xml_data = etree.tostring(root.find(element.tag))
                sub_obj = sub_obj.from_xml(sub_xml_data)
                setattr(obj, element.tag, sub_obj)

            elif element.tag in obj.list_dict:
                sub_list = []
                for elem in root.findall(element.tag):
                    sub_xml_data = etree.tostring(elem)

                    if 'DetailType' in elem.keys() and elem.get('DetailType') in obj.detail_dict:
                        sub_obj = obj.detail_dict[elem.get('DetailType')]()
                    else:
                        sub_obj = obj.list_dict[element.tag]()

                    sub_obj = sub_obj.from_xml(sub_xml_data)
                    sub_list.append(sub_obj)

                setattr(obj, element.tag, sub_list)
            else:
                setattr(obj, element.tag, root.getchildren()[0].text)
        return obj



# Based on http://stackoverflow.com/a/1118038
def to_dict(obj, classkey=None):
    """
    Recursively converts Python object into a dictionary
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_dict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, to_dict(value, classkey))
                    for key, value in obj.__dict__.items()
                    if not callable(value) and not key.startswith('_')])

        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

class ToDictMixin(object):
    def to_dict(self):
        return to_dict(self)
