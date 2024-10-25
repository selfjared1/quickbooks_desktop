from lxml import etree as et
from sqlalchemy import func

from src.quickbooks_desktop.qb_special_fields import QBDates
from src.quickbooks_desktop.conversions import qb_to_sql
from src.quickbooks_desktop.mixins.qb_mixins import logger


class PluralMixin:

    # class Meta:
    #     name = ''
    #     plural_of = ''
    #     plural_of_db_model = ''


    def __init__(self):
        self._items = []

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        return len(self._items)

    def add_item(self, item):
        self._items.append(item)

    @classmethod
    def from_list(cls, items):
        instance = cls()
        for item in items:
            instance.add_item(item)
        return instance

    @classmethod
    def get_all_from_qb(cls, qb, include_custom_fields=False, include_line_items=False, include_linked_txns=False):
        QueryRq = et.Element(f'{cls.Meta.name}QueryRq')
        if include_line_items:
            custom_query = et.SubElement(QueryRq, 'IncludeLineItems')
            custom_query.text = 'true'
        else:
            pass

        if include_linked_txns:
            custom_query = et.SubElement(QueryRq, 'IncludeLinkedTxns')
            custom_query.text = 'true'
        else:
            pass

        if include_custom_fields:
            custom_query = et.SubElement(QueryRq, 'OwnerID')
            custom_query.text = '0' #zero is the ownerID for all custom fields (not private fields)
        else:
            pass

        QueryRs_list = qb.send_xml(QueryRq)
        if type(QueryRs_list) == list and len(QueryRs_list) == 1:
            QueryRs = QueryRs_list[0]
            plural_instance = cls()
            for Ret in QueryRs:
                obj = plural_instance.Meta.plural_of.from_xml(Ret)
                plural_instance._items.append(obj)
            return plural_instance
        else:
            logger.debug(f"QueryRs_list is of type {type(QueryRs_list)} instead of list type")

    def to_list(self):
        return self._items

    @classmethod
    def from_xml(cls, list_of_ret):
        """A Ret should be passed in but it's sometimes not."""
        if not isinstance(list_of_ret, list):
            logger.debug(f'from_xml expects a list. Ret must be an instance of lxml.etree._Element. Your Ret is type {type(list_of_ret)}')
            logger.debug(f'list_of_ret is {list_of_ret}')
            raise TypeError(f'Ret must be an instance of lxml.etree._Element. Your Ret is type {type(list_of_ret)}')
        elif not len(list_of_ret):
            plural_instance = cls()
            return plural_instance
        elif list_of_ret[0].tag[-3:] != 'Ret':
            raise ValueError(f"Invalid tag: {list_of_ret[0].tag}. Must end with 'Ret' (as in RETurn from Quickbooks).")
        else:
            plural_instance = cls()
            for instance_xml in list_of_ret:
                plural_of_class = cls.Meta.plural_of
                plural_of_instance = plural_of_class.from_xml(instance_xml)
                plural_instance._items.append(plural_of_instance)
            return plural_instance

    def to_db(self, session=None):
        logger.debug('Began to_db')
        sqlalchemy_instances = []
        for dataclass_instance in self._items:
            sqlalchemy_instance = qb_to_sql(dataclass_instance, self.Meta.plural_of_db_model)
            sqlalchemy_instances.append(sqlalchemy_instance)
        logger.debug('Created sqlalchemy_instances.')
        with session.no_autoflush:
            for instance in sqlalchemy_instances:
                existing_instance = session.query(self.Meta.plural_of_db_model).filter_by(list_id=instance.list_id).first()
                if existing_instance:
                    # Delete the existing entry
                    session.delete(existing_instance)
                    session.commit()
                else:
                    pass
                session.add(instance)
            # # Commit the changes
            session.commit()
        logger.debug('Finished to_db')


    @classmethod
    def __get_last_time_modified_from_db(cls, session):
        max_time_modified = session.query(func.max(cls.Meta.plural_of_db_model.time_modified)).scalar()
        qb_max_time_modified = QBDates(max_time_modified)
        return qb_max_time_modified

    @classmethod
    def __get_from_qb_since_last_time_modified(cls, qb_max_time_modified, qb):
        plural_instance = cls()
        query = plural_instance.Meta.plural_of.Query()
        query.from_modified_date = qb_max_time_modified
        query_xml = query.to_xml()
        QueryRs = qb.send_xml(query_xml)
        for Ret in QueryRs:
            obj = plural_instance.Meta.plural_of.from_xml(Ret)
            plural_instance._items.append(obj)
        return plural_instance

    @classmethod
    def update_db(cls, qb, session):
        qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
        plural_instance = cls.__get_from_qb_since_last_time_modified(qb_max_time_modified, qb)
        plural_instance.to_db(session)

    @classmethod
    def populate_db(cls, qb, session):
        instances = cls.get_all_from_qb(qb)
        instances.to_db(session)

    @classmethod
    def populate_or_update_db(cls, qb, session):
        qb_max_time_modified = cls.__get_last_time_modified_from_db(session)
        if qb_max_time_modified:
            cls.update_db(qb, session)
        else:
            cls.populate_db(qb, session)

    def to_xml(self):
        """
        Converts all items in the plural mixin into a list of lxml elements
        by calling each child's `to_xml` method.
        """
        xml_elements = []
        for item in self._items:
            xml_element = item.to_xml()  # Each item must implement `to_xml`
            xml_elements.append(xml_element)
        return xml_elements

    def to_xml_file(self, file_path: str) -> None:
        """
        Generates an XML file with the plural objects.
        Creates a root element based on the Meta class name, appends all items, and writes to the file path.

        Args:
            file_path (str): The path of the file to write the XML to. The file will be replaced if it exists.
        """
        # Convert each child to an XML element
        list_of_xml = self.to_xml()

        # Create the root element using the Meta class name
        root = et.Element(f"{self.Meta.name}QueryRs")

        # Append each child XML element to the root
        for xml_element in list_of_xml:
            root.append(xml_element)

        # Convert the root element to a formatted XML string
        xml_str = et.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

        # Write the XML string to the specified file path, replacing the file if it exists
        with open(file_path, "w") as file:
            file.write(xml_str)

        logger.debug('Finished to_xml_file')


class PluralListSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for item in self:
            if item.list_id is not None:
                mod_xml = item._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = item._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

class PluralTrxnSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for trxn in self:
            if trxn.trxn_id is not None:
                mod_xml = trxn._get_mod_rq_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = trxn._get_add_rq_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

    def add_all(self, qb):
        xml_requests = []
        for trxn in self:
            add_xml = trxn._get_add_rq_xml()
            xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response

    def set_ids_to_none(self, id_name):
        # Iterate over each item in the _items list, assuming they are instances of some class
        for item in self:
            self._set_list_id_in_instance_to_none(item, id_name)

    def _set_list_id_in_instance_to_none(self, obj, id_name):
        # Iterate through all attributes of the object
        for attr_name in dir(obj):
            if attr_name.startswith('__'):
                pass
            elif attr_name.startswith('_'):
                pass
            elif attr_name in ['Add', 'Mod', 'Query', 'Meta', 'IS_YES_NO_FIELD_LIST']:
                pass
            elif attr_name.endswith('Ref') or attr_name.endswith('ref'):
                ref = getattr(obj, attr_name)
                if hasattr(ref, id_name):
                    ref.list_id = None
                else:
                    pass
            else:
                attr_value = getattr(obj, attr_name)

                # If the attribute is a list, iterate through the list items
                if isinstance(attr_value, list):
                    for sub_item in attr_value:
                        if hasattr(sub_item, id_name):
                            setattr(sub_item, id_name, None)
                        else:
                            pass
                        self._set_list_id_in_instance_to_none(sub_item, id_name)  # Recurse for nested objects

                # If the attribute itself has a 'list_id', set it to None
                elif hasattr(attr_value, id_name):
                    setattr(attr_value, id_name, None)

                else:

                    # If the attribute is 'list_id', set it to None
                    if attr_name == id_name:
                        setattr(obj, attr_name, None)
                    else:
                        pass



