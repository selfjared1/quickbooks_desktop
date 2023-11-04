import unittest
from datetime import datetime
from transactions.TimeTracking import TimeTrackingQueryRq

class TestTimeTrackingQueryRq(unittest.TestCase):

    def test_attributes(self):
        query = TimeTrackingQueryRq(
            TxnID="ID1",
            TimeCreated=datetime(2021, 1, 1, 0, 0, 0),
            TimeModified=datetime(2021, 12, 31, 23, 59, 59),
            EditSequence="EditSeq1",
            TxnNumber=123,
            TxnDate=datetime(2021, 1, 1).date(),
            defMacro="Macro1",
            EntityRef_ListID="ListID1",
            EntityRef_FullName="FullName1",
            CustomerRef_ListID="ListID2",
            CustomerRef_FullName="FullName2",
            ItemServiceRef_ListID="ListID3",
            ItemServiceRef_FullName="FullName3",
            Duration="Duration1",
            ClassRef_ListID="ListID4",
            ClassRef_FullName="FullName4",
            PayrollItemWageRef_ListID="ListID5",
            PayrollItemWageRef_FullName="FullName5",
            Notes="Notes1",
            BillableStatus="Billable",
            IsBillable=True,
            ExternalGUID="GUID1",
            IncludeRetElement=["IncludeRetElement1", "IncludeRetElement2"],
            IsBilled=True,
            ErrorRecovery_ListID="ListID6",
            ErrorRecovery_OwnerID="OwnerID1",
            ErrorRecovery_TxnID="TxnID2",
            ErrorRecovery_TxnNumber=124,
            ErrorRecovery_EditSequence="EditSeq2",
            ErrorRecovery_ExternalGUID="GUID2",
            statusCode=200,
            statusSeverity="Info",
            statusMessage="StatusMessage1"
        )

        self.assertEqual(query.TxnID, "ID1")
        self.assertEqual(query.TimeCreated, datetime(2021, 1, 1, 0, 0, 0))
        self.assertEqual(query.TimeModified, datetime(2021, 12, 31, 23, 59, 59))
        self.assertEqual(query.EditSequence, "EditSeq1")
        self.assertEqual(query.TxnNumber, 123)
        self.assertEqual(query.TxnDate, datetime(2021, 1, 1).date())
        self.assertEqual(query.defMacro, "Macro1")
        self.assertEqual(query.EntityRef_ListID, "ListID1")
        self.assertEqual(query.EntityRef_FullName, "FullName1")
        self.assertEqual(query.CustomerRef_ListID, "ListID2")
        self.assertEqual(query.CustomerRef_FullName, "FullName2")
        self.assertEqual(query.ItemServiceRef_ListID, "ListID3")
        self.assertEqual(query.ItemServiceRef_FullName, "FullName3")
        self.assertEqual(query.Duration, "Duration1")
        self.assertEqual(query.ClassRef_ListID, "ListID4")
        self.assertEqual(query.ClassRef_FullName, "FullName4")
        self.assertEqual(query.PayrollItemWageRef_ListID, "ListID5")
        self.assertEqual(query.PayrollItemWageRef_FullName, "FullName5")
        self.assertEqual(query.Notes, "Notes1")
        self.assertEqual(query.BillableStatus, "Billable")
        self.assertEqual(query.IsBillable, True)
        self.assertEqual(query.ExternalGUID, "GUID1")
        self.assertEqual(query.IncludeRetElement, ["IncludeRetElement1", "IncludeRetElement2"])
        self.assertEqual(query.IsBilled, True)
        self.assertEqual(query.ErrorRecovery_ListID, "ListID6")
        self.assertEqual(query.ErrorRecovery_OwnerID, "OwnerID1")
        self.assertEqual(query.ErrorRecovery_TxnID, "TxnID2")
        self.assertEqual(query.ErrorRecovery_TxnNumber, 124)
        self.assertEqual(query.ErrorRecovery_EditSequence, "EditSeq2")
        self.assertEqual(query.ErrorRecovery_ExternalGUID, "GUID2")
        self.assertEqual(query.statusCode, 200)
        self.assertEqual(query.statusSeverity, "Info")
        self.assertEqual(query.statusMessage, "StatusMessage1")

    # def test_from_xml(self):
    #     xml_string = """
    #     <TimeTrackingQueryRq metaData="MetaDataValue" iterator="IteratorValue" iteratorID="IteratorIDValue">
    #         <TxnID>IDValue</TxnID>
    #         <MaxReturned>10</MaxReturned>
    #         <ModifiedDateRangeFilter>
    #             <FromModifiedDate>2022-01-01T00:00:00</FromModifiedDate>
    #             <ToModifiedDate>2022-12-31T23:59:59</ToModifiedDate>
    #         </ModifiedDateRangeFilter>
    #         <TxnDateRangeFilter>
    #             <FromTxnDate>2022-01-01</FromTxnDate>
    #             <ToTxnDate>2022-12-31</ToTxnDate>
    #             <DateMacro>Today</DateMacro>
    #         </TxnDateRangeFilter>
    #         <TimeTrackingEntityFilter>
    #             <ListID>ListIDValue</ListID>
    #             <FullName>FullNameValue</FullName>
    #         </TimeTrackingEntityFilter>
    #         <IncludeRetElement>IncludeElementValue</IncludeRetElement>
    #     </TimeTrackingQueryRq>
    #     """
    #     query = TimeTrackingQueryRq.from_xml(xml_string)
    #     self.assertEqual(query.metaData, "ENUMTYPE")
    #     self.assertEqual(query.iterator, "ENUMTYPE")
    #     self.assertEqual(query.iteratorID, "UUIDTYPE")
    #     self.assertEqual(query.TxnID, ["IDTYPE"])
    #     self.assertEqual(query.MaxReturned, 10)
    #     self.assertEqual(query.FromModifiedDate, datetime.strptime("DATETIMETYPE", '%Y-%m-%dT%H:%M:%S'))
    #     self.assertEqual(query.ToModifiedDate, datetime.strptime("DATETIMETYPE", '%Y-%m-%dT%H:%M:%S'))
    #     self.assertEqual(query.FromTxnDate, datetime.strptime("DATETYPE", '%Y-%m-%d').date())
    #     self.assertEqual(query.ToTxnDate, datetime.strptime("DATETYPE", '%Y-%m-%d').date())
    #     self.assertEqual(query.DateMacro, "ENUMTYPE")
    #     self.assertEqual(query.ListID, ["IDTYPE"])
    #     self.assertEqual(query.FullName, ["STRTYPE"])
    #     self.assertEqual(query.IncludeRetElement, ["STRTYPE"])

if __name__ == '__main__':
    unittest.main()