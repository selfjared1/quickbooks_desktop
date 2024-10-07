from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for all the models
Base = declarative_base()

# Define the model with request_id, old_id, new_id
class TransactionMapping(Base):
    __tablename__ = 'transaction_mapping'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    request_id = Column(Integer, nullable=False)
    qb_add_rq_name = Column(String, nullable=False)
    is_trx_line_id = Column(Boolean, nullable=False)
    old_qb_id = Column(String, nullable=False, unique=True)
    new_qb_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<TransactionMapping(request_id={self.request_id}, old_id={self.old_id}, new_id={self.new_id})>"


class DataExtMod(Base):
    __tablename__ = 'data_ext_mod'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_ext_name = Column(String, nullable=False)
    txn_data_ext_type = Column(String, nullable=False)
    txn_id_old = Column(String, nullable=False, unique=True)
    txn_id_new = Column(String, nullable=True, unique=True)
    txn_line_id_old = Column(String, nullable=True, unique=True)
    txn_line_id_new = Column(String, nullable=True, unique=True)
    data_ext_value = Column(String, nullable=True)

    def __repr__(self):
        return (f"<DataExtMod(id={self.id}, data_ext_name={self.data_ext_name}, "
                f"txn_data_ext_type={self.txn_data_ext_type}, txn_id_old={self.txn_id_old}, "
                f"txn_id_new={self.txn_id_new}, txn_line_id_old={self.txn_line_id_old}, "
                f"txn_line_id_new={self.txn_line_id_new}, data_ext_value={self.data_ext_value})>")
