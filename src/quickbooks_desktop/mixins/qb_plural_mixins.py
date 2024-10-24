from lxml import etree as et
from sqlalchemy import func

from src.quickbooks_desktop.common_and_special_fields.qb_special_fields import QBDates
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
    def get_all_from_qb(cls, qb, include_custom_fields=False):
        QueryRq = et.Element(f'{cls.Meta.name}QueryRq')
        if include_custom_fields:
            custom_query = et.SubElement(QueryRq, 'OwnerID')
            custom_query.text = '0' #zero is the ownerID for all custom fields (not private fields)
        QueryRs = qb.send_xml(QueryRq)
        plural_instance = cls()
        for Ret in QueryRs:
            obj = plural_instance.Meta.plural_of.from_xml(Ret)
            plural_instance._items.append(obj)
        return plural_instance

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


class PluralListSaveMixin:
    def save_all(self, qb):
        xml_requests = []
        for item in self:
            if item.list_id is not None:
                mod_xml = item._get_mod_xml()
                xml_requests.append(mod_xml)
            else:
                add_xml = item._get_add_xml()
                xml_requests.append(add_xml)
        response = qb.send_xml(xml_requests)
        return response
