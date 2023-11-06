import unittest
from core.base import QBBaseMixin, QBListBase, QBContactBase, QBAddressBlock, QBAddress, QBTransactionBase
from core.special_fields import QBDate, DataExtRet


class TestQBBaseMixin(unittest.TestCase):
    def test_default_values(self):
        """Test the default values are None."""
        base_mixin = QBBaseMixin()
        self.assertIsNone(base_mixin.TimeCreated)
        self.assertIsNone(base_mixin.TimeModified)
        self.assertIsNone(base_mixin.EditSequence)
        self.assertIsNone(base_mixin.DataExtRet)

    def test_assigned_values(self):
        """Test that values can be assigned correctly."""
        time_created = QBDate('1/1/2023')
        time_modified = QBDate('1/1/2023')
        edit_sequence = '123456'
        data_ext_ret = DataExtRet()  # Assuming DataExtRet is properly defined elsewhere

        base_mixin = QBBaseMixin(
            TimeCreated=time_created,
            TimeModified=time_modified,
            EditSequence=edit_sequence,
            DataExtRet=data_ext_ret
        )

        self.assertEqual(base_mixin.TimeCreated, time_created)
        self.assertEqual(base_mixin.TimeModified, time_modified)
        self.assertEqual(base_mixin.EditSequence, edit_sequence)
        self.assertEqual(base_mixin.DataExtRet, data_ext_ret)

class TestQBListBase(unittest.TestCase):
    def test_default_values(self):
        """Test that the default values are correctly assigned."""
        list_base = QBListBase()
        self.assertIsNone(list_base.ListID)
        self.assertIsNone(list_base.Name)
        self.assertIsNone(list_base.IsActive)

        # Also testing inheritance properties from QBBaseMixin
        self.assertIsNone(list_base.TimeCreated)
        self.assertIsNone(list_base.TimeModified)
        self.assertIsNone(list_base.EditSequence)
        self.assertIsNone(list_base.DataExtRet)

    def test_assigned_values(self):
        """Test that values are correctly assigned when provided."""
        list_base = QBListBase(
            ListID='123',
            Name='Test Name',
            IsActive=True
        )

        self.assertEqual(list_base.ListID, '123')
        self.assertEqual(list_base.Name, 'Test Name')
        self.assertTrue(list_base.IsActive)

    def test_inheritance(self):
        time_created = QBDate('1/1/2023')
        list_base = QBListBase(TimeCreated=time_created)
        self.assertEqual(list_base.TimeCreated, time_created)

class TestQBContactBase(unittest.TestCase):
    def test_default_values(self):
        """Test that the default values are None."""
        contact_base = QBContactBase()
        self.assertIsNone(contact_base.CompanyName)
        self.assertIsNone(contact_base.Salutation)
        self.assertIsNone(contact_base.FirstName)
        self.assertIsNone(contact_base.MiddleName)
        self.assertIsNone(contact_base.LastName)
        self.assertIsNone(contact_base.Phone)
        self.assertIsNone(contact_base.Email)
        self.assertIsNone(contact_base.AccountNumber)

        # Inherited attributes should also be None by default
        self.assertIsNone(contact_base.ListID)
        self.assertIsNone(contact_base.Name)
        self.assertIsNone(contact_base.IsActive)

    def test_assigned_values(self):
        """Test that the assigned values are set correctly."""
        contact_base = QBContactBase(
            CompanyName='Test Company',
            Salutation='Mr.',
            FirstName='John',
            MiddleName='T.',
            LastName='Doe',
            Phone='123-456-7890',
            Email='john.doe@example.com',
            AccountNumber='ACC123'
        )

        self.assertEqual(contact_base.CompanyName, 'Test Company')
        self.assertEqual(contact_base.Salutation, 'Mr.')
        self.assertEqual(contact_base.FirstName, 'John')
        self.assertEqual(contact_base.MiddleName, 'T.')
        self.assertEqual(contact_base.LastName, 'Doe')
        self.assertEqual(contact_base.Phone, '123-456-7890')
        self.assertEqual(contact_base.Email, 'john.doe@example.com')
        self.assertEqual(contact_base.AccountNumber, 'ACC123')

class TestQBAddressBlock(unittest.TestCase):
    def test_default_values(self):
        """Test that the default values for address lines are None."""
        address_block = QBAddressBlock()
        self.assertIsNone(address_block.Addr1)
        self.assertIsNone(address_block.Addr2)
        self.assertIsNone(address_block.Addr3)
        self.assertIsNone(address_block.Addr4)
        self.assertIsNone(address_block.Addr5)

    def test_assigned_values(self):
        """Test that the assigned values for address lines are correctly set."""
        address_block = QBAddressBlock(
            Addr1='123 Main St',
            Addr2='Unit 4',
            Addr3='Business Park',
            Addr4='Springfield',
            Addr5='IL'
        )
        self.assertEqual(address_block.Addr1, '123 Main St')
        self.assertEqual(address_block.Addr2, 'Unit 4')
        self.assertEqual(address_block.Addr3, 'Business Park')
        self.assertEqual(address_block.Addr4, 'Springfield')
        self.assertEqual(address_block.Addr5, 'IL')

class TestQBAddress(unittest.TestCase):
    def test_default_values(self):
        """Test that the default values for all fields are None."""
        address = QBAddress()
        self.assertIsNone(address.Addr1)
        self.assertIsNone(address.Addr2)
        self.assertIsNone(address.Addr3)
        self.assertIsNone(address.Addr4)
        self.assertIsNone(address.Addr5)
        self.assertIsNone(address.City)
        self.assertIsNone(address.State)
        self.assertIsNone(address.PostalCode)
        self.assertIsNone(address.Country)
        self.assertIsNone(address.Note)

    def test_assigned_values(self):
        """Test that the assigned values are set correctly."""
        address = QBAddress(
            Addr1='123 Main St',
            Addr2='Unit 4',
            Addr3='Business Park',
            Addr4='Springfield',
            Addr5='IL',
            City='Springfield',
            State='IL',
            PostalCode='62704',
            Country='USA',
            Note='Deliver to the rear entrance.'
        )
        self.assertEqual(address.Addr1, '123 Main St')
        self.assertEqual(address.Addr2, 'Unit 4')
        self.assertEqual(address.Addr3, 'Business Park')
        self.assertEqual(address.Addr4, 'Springfield')
        self.assertEqual(address.Addr5, 'IL')
        self.assertEqual(address.City, 'Springfield')
        self.assertEqual(address.State, 'IL')
        self.assertEqual(address.PostalCode, '62704')
        self.assertEqual(address.Country, 'USA')
        self.assertEqual(address.Note, 'Deliver to the rear entrance.')

class TestQBTransactionBase(unittest.TestCase):
    def test_default_values(self):
        """Test that the default values for transaction attributes are None."""
        transaction_base = QBTransactionBase()
        self.assertIsNone(transaction_base.TxnID)
        self.assertIsNone(transaction_base.TxnDate)

        # Test inherited attributes from QBBaseMixin
        self.assertIsNone(transaction_base.TimeCreated)
        self.assertIsNone(transaction_base.TimeModified)
        self.assertIsNone(transaction_base.EditSequence)
        self.assertIsNone(transaction_base.DataExtRet)

    def test_assigned_values(self):
        """Test that the assigned values are set correctly."""
        txn_id = 'TXN123'
        txn_date = QBDate('1/1/2023')  # Replace with the correct QBDate initialization

        transaction_base = QBTransactionBase(
            TxnID=txn_id,
            TxnDate=txn_date
        )

        self.assertEqual(transaction_base.TxnID, txn_id)
        self.assertEqual(transaction_base.TxnDate, txn_date)

