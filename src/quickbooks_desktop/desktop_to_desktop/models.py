from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for all the models
Base = declarative_base()

# Define the model with request_id, old_id, new_id
class TransactionMapping(Base):
    __tablename__ = 'transaction_mapping'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    request_id = Column(Integer, nullable=False)  # The request ID
    old_id = Column(String, nullable=False)  # The old ID
    new_id = Column(String, nullable=False)  # The new ID

    def __repr__(self):
        return f"<TransactionMapping(request_id={self.request_id}, old_id={self.old_id}, new_id={self.new_id})>"

# Example of setting up the SQLite database (you can change to another DB if needed)
engine = create_engine('sqlite:///transactions.db', echo=True)

# Create the table in the database
Base.metadata.create_all(engine)