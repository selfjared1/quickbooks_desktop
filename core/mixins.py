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
    def to_xml(self, name_of_start_tag=None):
        if name_of_start_tag is None:
            name_of_start_tag = self.__class__.__name__
        else:
            name_of_start_tag = name_of_start_tag.replace('_', '')
        root = etree.Element(name_of_start_tag)
        for key, value in vars(self).items():
            if not key.startswith('_') and value is not None:
                child = etree.SubElement(root, key)
                child.text = str(value)
            else:
                pass
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')

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
        for key in root.keys():
            if key in obj.class_dict:
                sub_obj = obj.class_dict[key]()
                sub_xml_data = etree.tostring(root.find(key))
                sub_obj = sub_obj.from_xml(sub_xml_data)
                setattr(obj, key, sub_obj)

            elif key in obj.list_dict:
                sub_list = []
                for elem in root.findall(key):
                    sub_xml_data = etree.tostring(elem)

                    if 'DetailType' in elem.keys() and elem.get('DetailType') in obj.detail_dict:
                        sub_obj = obj.detail_dict[elem.get('DetailType')]()
                    else:
                        sub_obj = obj.list_dict[key]()

                    sub_obj = sub_obj.from_xml(sub_xml_data)
                    sub_list.append(sub_obj)

                setattr(obj, key, sub_list)
            else:
                setattr(obj, key, root.get(key))

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
