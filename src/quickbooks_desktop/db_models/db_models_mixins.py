import logging
logger = logging.getLogger(__name__)

class ModelMixin:
    def to_db(self, session):
        session.add(self)
        session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class PluralMixin:

    class Meta:
        name = ""
        plural_of_db_model = object

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

    def add_item_and_save(self, item, session):
        item.to_db(session)
        self.add_item(item)

    def add_items(self, items):
        # assuming items is a list
        self._items.extend(items)

    def add_items_and_save(self, items, session):
        for item in items:
            item.to_db(session)
            self.add_item(item)

    def to_db(self, session):
        if len(self._items):
            session.add_all(self._items)
        else:
            raise Exception('No items to save')

    @classmethod
    def get_all(cls, session):
        plural_instance = cls()
        list_from_db = session.query(cls.Meta.plural_of_db_model).all()
        plural_instance.add_items(list_from_db)
        return plural_instance

    @classmethod
    def truncate(cls, session):
        """Remove all records from the database for this class."""
        try:
            # Perform the delete operation
            session.query(cls.Meta.plural_of_db_model).delete()
            session.commit()
            logger.info(f"All records for {cls.Meta.plural_of_db_model.__name__} have been deleted.")
        except Exception as e:
            logger.error(f"Error truncating table for {cls.Meta.plural_of_db_model.__name__}: {e}")
            session.rollback()