import unittest
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
from src.quickbooks_desktop.transactions.invoices import Invoices


class test_query(unittest.TestCase):

    def test_query_invoices(self):
        qb = QuickbooksDesktop()
        invoices = Invoices.get_all_from_qb(qb)

        self.assertIsNotNone(len(invoices))
