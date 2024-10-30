from typing import Type, Any
from sqlalchemy.orm import Session
from dataclasses import fields, is_dataclass, MISSING
from src.quickbooks_desktop.db_models.base import Base
from src.quickbooks_desktop.qb_special_fields import QBDates, QBTime


import logging

logger = logging.getLogger(__name__)

def create_address(dataclass_instance):
    from src.quickbooks_desktop.common.qb_contact_common import Address
    address = Address()
    try:
        for field in fields(dataclass_instance):
            field_value = getattr(dataclass_instance, field.name)
            setattr(address, field.name, field_value)
        setattr(address, 'address_type', dataclass_instance.Meta.name)
        return address
    except Exception as e:
        return None

def qb_to_sql(dataclass_instance: Any, db_model: Type[Base]) -> Base:
    """
    Convert a dataclass instance to a SQLAlchemy model instance.

    Args:
    - dataclass_instance (Any): The dataclass instance to convert.
    - plural_of_db_model (Type[Base]): The target SQLAlchemy model class.
    - session (Session): The SQLAlchemy session to use for relationships.

    Returns:
    - Base: The SQLAlchemy model instance.
    """
    if not is_dataclass(dataclass_instance):
        raise ValueError("Provided instance is not a dataclass instance.")

    sqlalchemy_instance = db_model()

    for field in fields(dataclass_instance):
        field_value = getattr(dataclass_instance, field.name)

        if 'address' in field.name:
            if field_value is None:
                continue
            elif isinstance(field_value, list) and not len(field_value):
                continue
            else:
                address = create_address(field_value)
                if address is not None:
                    getattr(sqlalchemy_instance, 'addresses').append(address)
                else:
                    continue
        elif isinstance(field_value, list) and len(field_value):
            # Handle lists (assumed to be relationships)
            sqlalchemy_related_class = getattr(db_model, field.name).mapper.class_
            related_instances = [qb_to_sql(item, sqlalchemy_related_class) for item in field_value]
            setattr(sqlalchemy_instance, field.name, related_instances)
        elif isinstance(field_value, QBDates):
            setattr(sqlalchemy_instance, field.name, field_value.date)
        elif isinstance(field_value, QBTime):
            setattr(sqlalchemy_instance, field.name, field_value.to_float_hours())
        elif is_dataclass(field_value) and field.name[-3:] == 'ref':
            if field.name not in ['additional_contact_ref']:
                setattr(sqlalchemy_instance, str(field.name + '_list_id'), field_value.list_id)
                setattr(sqlalchemy_instance, str(field.name + '_full_name'), field_value.full_name)
            else:
                #todo:
                pass
        elif is_dataclass(field_value):
            # Handle nested dataclasses
            try:
                sqlalchemy_related_class = getattr(db_model, field.name).mapper.class_
                related_instance = qb_to_sql(field_value, sqlalchemy_related_class)
                setattr(sqlalchemy_instance, field.name, related_instance)
            except Exception as e:
                print(e)
                print(f'db_model={db_model}, field_value={field_value}')
                print(f'field.name={field.name}')
                print(f'sqlalchemy_instance={sqlalchemy_instance}')
        else:
            # Direct field assignment
            setattr(sqlalchemy_instance, field.name, field_value)

    return sqlalchemy_instance


def sql_to_qb(sqlalchemy_instance: Base, dataclass_type: Type[Any], session: Session) -> Any:
    """
    Convert a SQLAlchemy model instance to a dataclass instance.

    Args:
    - sqlalchemy_instance (Base): The SQLAlchemy model instance to convert.
    - dataclass_type (Type[Any]): The target dataclass type.
    - session (Session): The SQLAlchemy session to use for relationships.

    Returns:
    - Any: The dataclass instance.
    """
    if not is_dataclass(dataclass_type):
        raise ValueError("Provided type is not a dataclass type.")

    init_args = {}

    for field in fields(dataclass_type):
        field_value = getattr(sqlalchemy_instance, field.name, MISSING)

        if field_value is MISSING:
            continue

        if isinstance(field_value, list):
            # Handle lists (assumed to be relationships)
            dataclass_related_type = field.type.__args__[0]
            related_instances = [sql_to_qb(item, dataclass_related_type, session) for item in field_value]
            init_args[field.name] = related_instances
        elif hasattr(field.type, '__dataclass_fields__'):
            # Handle nested dataclasses
            related_instance = sql_to_qb(field_value, field.type, session)
            init_args[field.name] = related_instance
        else:
            # Direct field assignment
            init_args[field.name] = field_value

    return dataclass_type(**init_args)