import unittest
from lists.account_open_ai_complex import AccountQueryRq

class TestAccountQueryRq(unittest.TestCase):

    def test_valid_account_query_rq(self):
        # Prepare valid input data
        data = {
            "meta_data": "ENUMTYPE",
            "list_id": ["IDTYPE1", "IDTYPE2"],
            "max_returned": 10,
            "active_status": "ActiveOnly",
            "from_modified_date": "2021-01-01T12:00:00-07:00",
            "to_modified_date": "2022-01-01T12:00:00-07:00",
            "name_filter": {
                "match_criterion": "StartsWith",
                "name": "Acme"
            },
            "account_type": ["AccountsPayable", "Expense"],
            "currency_filter": {
                "list_id": ["IDTYPE1", "IDTYPE2"],
                "full_name": ["USD", "EUR"]
            },
            "include_ret_element": ["ListID", "Name"],
            "owner_id": ["GUID1", "GUID2"]
        }

        # Create an instance of the class
        query = AccountQueryRq.from_dict(data)

        # Check if the instance is valid
        errors = query.validate()
        self.assertEqual(len(errors), 0)

        # Check if the instance can be converted to a dictionary
        self.assertDictEqual(data, query.to_dict())

        # Check if the instance can be converted to XML
        xml_str = query.to_xml_string()
        self.assertIsNotNone(xml_str)

    def test_invalid_account_query_rq(self):
        # Prepare invalid input data
        data = {
            "meta_data": "INVALID",
            "list_id": "INVALID",
            "active_status": "INVALID",
            "from_modified_date": "INVALID",
            "to_modified_date": "INVALID",
            "name_filter": "INVALID",
            "account_type": "INVALID",
            "currency_filter": "INVALID",
            "include_ret_element": "INVALID",
            "owner_id": "INVALID"
        }

        # Create an instance of the class
        query = AccountQueryRq.from_dict(data)

        # Check if the instance is valid
        errors = query.validate()
        self.assertGreater(len(errors), 0)