import unittest
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop




class TestReports(unittest.TestCase):
    def setUp(self):
        self.sample_bs_standard_response = """<?xml version="1.0" ?>
            <QBXML>
                <QBXMLMsgsRs>
                    <GeneralSummaryReportQueryRs requestID="1" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
                        <ReportRet>
                            <ReportTitle>Balance Sheet</ReportTitle>
                            <ReportSubtitle>As of March 20, 2025</ReportSubtitle>
                            <ReportBasis>Accrual</ReportBasis>
                            <NumRows>71</NumRows>
                            <NumColumns>2</NumColumns>
                            <NumColTitleRows>1</NumColTitleRows>
                            <ColDesc colID="1" dataType="STRTYPE">
                                <ColTitle titleRow="1"/>
                                <ColType>Label</ColType>
                            </ColDesc>
                            <ColDesc colID="2" dataType="AMTTYPE">
                                <ColTitle titleRow="1" value="Mar 20, 25"/>
                                <ColType>Amount</ColType>
                            </ColDesc>
                            <ReportData>
                                <TextRow rowNumber="1" value="ASSETS"/>
                                <TextRow rowNumber="2" value="Current Assets"/>
                                <TextRow rowNumber="3" value="Checking/Savings"/>
                                <DataRow rowNumber="4">
                                    <RowData rowType="account" value="Cash Held in Bank"/>
                                    <ColData colID="1" value="Cash Held in Bank"/>
                                    <ColData colID="2" value="16125000.00"/>
                                </DataRow>
                                <DataRow rowNumber="5">
                                    <RowData rowType="account" value="Sample Ltd - Chase 3465"/>
                                    <ColData colID="1" value="Sample Ltd - Chase 3465"/>
                                    <ColData colID="2" value="994626.18"/>
                                </DataRow>
                                <DataRow rowNumber="6">
                                    <RowData rowType="account" value="Sample Ltd - Chase 5617"/>
                                    <ColData colID="1" value="Sample Ltd - Chase 5617"/>
                                    <ColData colID="2" value="280596.15"/>
                                </DataRow>
                                <SubtotalRow rowNumber="7">
                                    <ColData colID="1" value="Total Checking/Savings"/>
                                    <ColData colID="2" value="17400222.33"/>
                                </SubtotalRow>
                                <TextRow rowNumber="8" value="Accounts Receivable"/>
                                <DataRow rowNumber="9">
                                    <RowData rowType="account" value="Accounts Receivable"/>
                                    <ColData colID="1" value="Accounts Receivable"/>
                                    <ColData colID="2" value="1429770.85"/>
                                </DataRow>
                                <DataRow rowNumber="10">
                                    <RowData rowType="account" value="Allowance For Doubtful Accounts"/>
                                    <ColData colID="1" value="Allowance For Doubtful Accounts"/>
                                    <ColData colID="2" value="-21719.29"/>
                                </DataRow>
                                <SubtotalRow rowNumber="11">
                                    <ColData colID="1" value="Total Accounts Receivable"/>
                                    <ColData colID="2" value="1408051.56"/>
                                </SubtotalRow>
                                <TextRow rowNumber="12" value="Other Current Assets"/>
                                <DataRow rowNumber="13">
                                    <RowData rowType="account" value="Inventory Asset"/>
                                    <ColData colID="1" value="Inventory Asset"/>
                                    <ColData colID="2" value="1892653.68"/>
                                </DataRow>
                                <DataRow rowNumber="14">
                                    <RowData rowType="account" value="Prepaid Insurance"/>
                                    <ColData colID="1" value="Prepaid Insurance"/>
                                    <ColData colID="2" value="17748.74"/>
                                </DataRow>
                                <DataRow rowNumber="15">
                                    <RowData rowType="account" value="Prepaid Marketing"/>
                                    <ColData colID="1" value="Prepaid Marketing"/>
                                    <ColData colID="2" value="3483.33"/>
                                </DataRow>
                                <DataRow rowNumber="16">
                                    <RowData rowType="account" value="Prepaid Taxes - City"/>
                                    <ColData colID="1" value="Prepaid Taxes - City"/>
                                    <ColData colID="2" value="61496.56"/>
                                </DataRow>
                                <DataRow rowNumber="17">
                                    <RowData rowType="account" value="Prepaid Taxes - Federal"/>
                                    <ColData colID="1" value="Prepaid Taxes - Federal"/>
                                    <ColData colID="2" value="81983.25"/>
                                </DataRow>
                                <DataRow rowNumber="18">
                                    <RowData rowType="account" value="Prepaid Taxes - State"/>
                                    <ColData colID="1" value="Prepaid Taxes - State"/>
                                    <ColData colID="2" value="50687.50"/>
                                </DataRow>
                                <DataRow rowNumber="19">
                                    <RowData rowType="account" value="Prepaid Tradeshow"/>
                                    <ColData colID="1" value="Prepaid Tradeshow"/>
                                    <ColData colID="2" value="38142.57"/>
                                </DataRow>
                                <DataRow rowNumber="20">
                                    <RowData rowType="account" value="Undeposited Funds"/>
                                    <ColData colID="1" value="Undeposited Funds"/>
                                    <ColData colID="2" value="82832.46"/>
                                </DataRow>
                                <SubtotalRow rowNumber="21">
                                    <ColData colID="1" value="Total Other Current Assets"/>
                                    <ColData colID="2" value="2229028.09"/>
                                </SubtotalRow>
                                <SubtotalRow rowNumber="22">
                                    <ColData colID="1" value="Total Current Assets"/>
                                    <ColData colID="2" value="21037301.98"/>
                                </SubtotalRow>
                                <TextRow rowNumber="23" value="Fixed Assets"/>
                                <DataRow rowNumber="24">
                                    <RowData rowType="account" value="Accumulated Depreciation - ROU"/>
                                    <ColData colID="1" value="Accumulated Depreciation - ROU"/>
                                    <ColData colID="2" value="-44743.85"/>
                                </DataRow>
                                <DataRow rowNumber="25">
                                    <RowData rowType="account" value="Leased  Asset"/>
                                    <ColData colID="1" value="Leased  Asset"/>
                                    <ColData colID="2" value="157789.25"/>
                                </DataRow>
                                <SubtotalRow rowNumber="26">
                                    <ColData colID="1" value="Total Fixed Assets"/>
                                    <ColData colID="2" value="113045.40"/>
                                </SubtotalRow>
                                <TextRow rowNumber="27" value="Other Assets"/>
                                <DataRow rowNumber="28">
                                    <RowData rowType="account" value="Accu Amort - Customer List"/>
                                    <ColData colID="1" value="Accu Amort - Customer List"/>
                                    <ColData colID="2" value="-381410.00"/>
                                </DataRow>
                                <DataRow rowNumber="29">
                                    <RowData rowType="account" value="Accu Amort - Deveveloped Tech"/>
                                    <ColData colID="1" value="Accu Amort - Deveveloped Tech"/>
                                    <ColData colID="2" value="-2211364.04"/>
                                </DataRow>
                                <DataRow rowNumber="30">
                                    <RowData rowType="account" value="Accu Amort - Trademark"/>
                                    <ColData colID="1" value="Accu Amort - Trademark"/>
                                    <ColData colID="2" value="-212120.96"/>
                                </DataRow>
                                <DataRow rowNumber="31">
                                    <RowData rowType="account" value="Customer Relationships"/>
                                    <ColData colID="1" value="Customer Relationships"/>
                                    <ColData colID="2" value="8500000.00"/>
                                </DataRow>
                                <DataRow rowNumber="32">
                                    <RowData rowType="account" value="Developed Technology"/>
                                    <ColData colID="1" value="Developed Technology"/>
                                    <ColData colID="2" value="41700000.00"/>
                                </DataRow>
                                <DataRow rowNumber="33">
                                    <RowData rowType="account" value="Goodwill"/>
                                    <ColData colID="1" value="Goodwill"/>
                                    <ColData colID="2" value="24650276.76"/>
                                </DataRow>
                                <DataRow rowNumber="34">
                                    <RowData rowType="account" value="Investment in Subsidiary"/>
                                    <ColData colID="1" value="Investment in Subsidiary"/>
                                    <ColData colID="2" value="-76406628.40"/>
                                </DataRow>
                                <DataRow rowNumber="35">
                                    <RowData rowType="account" value="Leased  Asset Deposit"/>
                                    <ColData colID="1" value="Leased  Asset Deposit"/>
                                    <ColData colID="2" value="5130.00"/>
                                </DataRow>
                                <DataRow rowNumber="36">
                                    <RowData rowType="account" value="Trademarks"/>
                                    <ColData colID="1" value="Trademarks"/>
                                    <ColData colID="2" value="4000000.00"/>
                                </DataRow>
                                <SubtotalRow rowNumber="37">
                                    <ColData colID="1" value="Total Other Assets"/>
                                    <ColData colID="2" value="-356116.64"/>
                                </SubtotalRow>
                                <TotalRow rowNumber="38">
                                    <ColData colID="1" value="TOTAL ASSETS"/>
                                    <ColData colID="2" value="20794230.74"/>
                                </TotalRow>
                                <TextRow rowNumber="39" value="LIABILITIES &amp; EQUITY"/>
                                <TextRow rowNumber="40" value="Liabilities"/>
                                <TextRow rowNumber="41" value="Current Liabilities"/>
                                <TextRow rowNumber="42" value="Accounts Payable"/>
                                <DataRow rowNumber="43">
                                    <RowData rowType="account" value="Accounts Payable"/>
                                    <ColData colID="1" value="Accounts Payable"/>
                                    <ColData colID="2" value="442239.58"/>
                                </DataRow>
                                <SubtotalRow rowNumber="44">
                                    <ColData colID="1" value="Total Accounts Payable"/>
                                    <ColData colID="2" value="442239.58"/>
                                </SubtotalRow>
                                <TextRow rowNumber="45" value="Credit Cards"/>
                                <TextRow rowNumber="46" value="Amex"/>
                                <DataRow rowNumber="47">
                                    <RowData rowType="account" value="Amex:Amex sub"/>
                                    <ColData colID="1" value="Amex sub"/>
                                    <ColData colID="2" value="87.10"/>
                                </DataRow>
                                <SubtotalRow rowNumber="48">
                                    <RowData rowType="account" value="Amex"/>
                                    <ColData colID="1" value="Total Amex"/>
                                    <ColData colID="2" value="87.10"/>
                                </SubtotalRow>
                                <DataRow rowNumber="49">
                                    <RowData rowType="account" value="Amex Gold"/>
                                    <ColData colID="1" value="Amex Gold"/>
                                    <ColData colID="2" value="251.77"/>
                                </DataRow>
                                <DataRow rowNumber="50">
                                    <RowData rowType="account" value="Visa Card"/>
                                    <ColData colID="1" value="Visa Card"/>
                                    <ColData colID="2" value="52140.73"/>
                                </DataRow>
                                <SubtotalRow rowNumber="51">
                                    <ColData colID="1" value="Total Credit Cards"/>
                                    <ColData colID="2" value="52479.60"/>
                                </SubtotalRow>
                                <TextRow rowNumber="52" value="Other Current Liabilities"/>
                                <DataRow rowNumber="53">
                                    <RowData rowType="account" value="Accrued  Bonus"/>
                                    <ColData colID="1" value="Accrued  Bonus"/>
                                    <ColData colID="2" value="320335.80"/>
                                </DataRow>
                                <DataRow rowNumber="54">
                                    <RowData rowType="account" value="Accrued Bonus"/>
                                    <ColData colID="1" value="Accrued Bonus"/>
                                    <ColData colID="2" value="79687.00"/>
                                </DataRow>
                                <DataRow rowNumber="55">
                                    <RowData rowType="account" value="Accrued Commission"/>
                                    <ColData colID="1" value="Accrued Commission"/>
                                    <ColData colID="2" value="46153.91"/>
                                </DataRow>
                                <DataRow rowNumber="56">
                                    <RowData rowType="account" value="Accrued Group Employee Insuranc"/>
                                    <ColData colID="1" value="Accrued Group Employee Insuranc"/>
                                    <ColData colID="2" value="4845.28"/>
                                </DataRow>
                                <DataRow rowNumber="57">
                                    <RowData rowType="account" value="Contingent Consideration"/>
                                    <ColData colID="1" value="Contingent Consideration"/>
                                    <ColData colID="2" value="4450000.00"/>
                                </DataRow>
                                <DataRow rowNumber="58">
                                    <RowData rowType="account" value="Inter-Co"/>
                                    <ColData colID="1" value="Inter-Co"/>
                                    <ColData colID="2" value="219564.59"/>
                                </DataRow>
                                <DataRow rowNumber="59">
                                    <RowData rowType="account" value="Other Taxes Liabilities"/>
                                    <ColData colID="1" value="Other Taxes Liabilities"/>
                                    <ColData colID="2" value="173165.00"/>
                                </DataRow>
                                <DataRow rowNumber="60">
                                    <RowData rowType="account" value="Payroll Tax Liabilities"/>
                                    <ColData colID="1" value="Payroll Tax Liabilities"/>
                                    <ColData colID="2" value="1979.26"/>
                                </DataRow>
                                <SubtotalRow rowNumber="61">
                                    <ColData colID="1" value="Total Other Current Liabilities"/>
                                    <ColData colID="2" value="5295730.84"/>
                                </SubtotalRow>
                                <SubtotalRow rowNumber="62">
                                    <ColData colID="1" value="Total Current Liabilities"/>
                                    <ColData colID="2" value="5790450.02"/>
                                </SubtotalRow>
                                <TextRow rowNumber="63" value="Long Term Liabilities"/>
                                <DataRow rowNumber="64">
                                    <RowData rowType="account" value="Lease Liability"/>
                                    <ColData colID="1" value="Lease Liability"/>
                                    <ColData colID="2" value="114668.45"/>
                                </DataRow>
                                <SubtotalRow rowNumber="65">
                                    <ColData colID="1" value="Total Long Term Liabilities"/>
                                    <ColData colID="2" value="114668.45"/>
                                </SubtotalRow>
                                <SubtotalRow rowNumber="66">
                                    <ColData colID="1" value="Total Liabilities"/>
                                    <ColData colID="2" value="5905118.47"/>
                                </SubtotalRow>
                                <TextRow rowNumber="67" value="Equity"/>
                                <DataRow rowNumber="68">
                                    <RowData rowType="account" value="Retained Earnings"/>
                                    <ColData colID="1" value="Retained Earnings"/>
                                    <ColData colID="2" value="13536258.59"/>
                                </DataRow>
                                <DataRow rowNumber="69">
                                    <ColData colID="1" value="Net Income"/>
                                    <ColData colID="2" value="1352853.68"/>
                                </DataRow>
                                <SubtotalRow rowNumber="70">
                                    <ColData colID="1" value="Total Equity"/>
                                    <ColData colID="2" value="14889112.27"/>
                                </SubtotalRow>
                                <TotalRow rowNumber="71">
                                    <ColData colID="1" value="TOTAL LIABILITIES &amp; EQUITY"/>
                                    <ColData colID="2" value="20794230.74"/>
                                </TotalRow>
                            </ReportData>
                        </ReportRet>
                    </GeneralSummaryReportQueryRs>
                </QBXMLMsgsRs>
            </QBXML>
            """

    def test_report_creation(self):
        qb = QuickbooksDesktop()
        response_dict = qb._process_response(self.sample_bs_standard_response, 'instances_dict')
        bs_report = response_dict['GeneralSummaryReport'][0]
        self.assertEqual(bs_report.num_col_title_rows, 1)
        self.assertEqual(bs_report.num_columns, 2)
        self.assertEqual(bs_report.num_rows, 71)
        self.assertEqual(bs_report.report_basis, 'Accrual')
        self.assertIsNotNone(bs_report._report_data_xml)
        self.assertTrue(len(bs_report.col_desc)==2)
        self.assertIsNone(bs_report.col_desc[0].col_title[0].title_value)
        self.assertEqual(bs_report.col_desc[1].col_title[0].title_value, 'Mar 20, 25')

    def test_get_report_column_headers(self):
        qb = QuickbooksDesktop()
        response_dict = qb._process_response(self.sample_bs_standard_response, 'instances_dict')
        bs_report = response_dict['GeneralSummaryReport'][0]
        columns = bs_report._get_report_column_headers()
        expected_columns = ['Column01',"Mar 20, 25"]
        self.assertEqual(columns, expected_columns)

    def test_get_report_rows(self):
        qb = QuickbooksDesktop()
        response_dict = qb._process_response(self.sample_bs_standard_response, 'instances_dict')
        bs_report = response_dict['GeneralSummaryReport'][0]
        columns = bs_report._get_report_column_headers(with_row_type=True)
        rows = bs_report._get_report_rows(columns, with_row_type=True)

        expected_first_rows = [
            {'Column00': "TextRow", 'Column01': "ASSETS"},
            {'Column00': "TextRow", 'Column01': "Current Assets"},
            {'Column00': "TextRow", 'Column01': "Checking/Savings"},
            {'Column00': "account", 'Column01': "Cash Held in Bank", "Mar 20, 25": Decimal(16125000.00).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)},
            {'Column00': "account", 'Column01': "Sample Ltd - Chase 3465", "Mar 20, 25": Decimal(994626.18).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)},
            {'Column00': "account", 'Column01': "Sample Ltd - Chase 5617", "Mar 20, 25": Decimal(280596.15).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)},
            {'Column00': "SubtotalRow", 'Column01': "Total Checking/Savings", "Mar 20, 25": Decimal(17400222.33).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)},
        ]
        expected_first_df = pd.DataFrame(expected_first_rows)
        actual_first_df = pd.DataFrame(rows[:7])
        self.assertTrue(actual_first_df.equals(expected_first_df))


        expected_last_row = [
            {'Column00': "TotalRow", 'Column01': "TOTAL LIABILITIES & EQUITY", "Mar 20, 25": Decimal(20794230.74).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)},
        ]

        last_row = rows[-1:]
        self.assertEqual(expected_last_row, last_row)


    def test_report_to_df(self):
        qb = QuickbooksDesktop()
        response_dict = qb._process_response(self.sample_bs_standard_response, 'instances_dict')
        bs_report = response_dict['GeneralSummaryReport'][0]
        df = bs_report.to_dataframe()
        first_6 = df.head(6)
        first_6_sample = pd.DataFrame([{'Column01': 'ASSETS', 'Mar 20, 25': np.nan}, {'Column01': 'Current Assets', 'Mar 20, 25': np.nan}, {'Column01': 'Checking/Savings', 'Mar 20, 25': np.nan}, {'Column01': 'Cash Held in Bank', 'Mar 20, 25': Decimal('16125000.00')}, {'Column01': 'Sample Ltd - Chase 3465', 'Mar 20, 25': Decimal('994626.18')}, {'Column01': 'Sample Ltd - Chase 5617', 'Mar 20, 25': Decimal('280596.15')}])
        self.assertTrue(first_6.equals(first_6_sample))

        last_6 = df.tail(6).reset_index(drop=True)
        last_6_sample = pd.DataFrame([{'Column01': 'Total Liabilities', 'Mar 20, 25': Decimal('5905118.47')}, {'Column01': 'Equity', 'Mar 20, 25': np.nan}, {'Column01': 'Retained Earnings', 'Mar 20, 25': Decimal('13536258.59')}, {'Column01': 'Net Income', 'Mar 20, 25': Decimal('1352853.68')}, {'Column01': 'Total Equity', 'Mar 20, 25': Decimal('14889112.27')}, {'Column01': 'TOTAL LIABILITIES & EQUITY', 'Mar 20, 25': Decimal('20794230.74')}])
        self.assertTrue(last_6.equals(last_6_sample))

    # def test_get_report_file_open(self):
    #     """
    #     Only run this test if a company file is open.
    #     """
    #     qb = QuickbooksDesktop()
    #     report_query = GeneralSummaryReport.Query()
    #     report_query.general_summary_report_type = 'BalanceSheetStandard'
    #     report_query_xml = report_query.to_xml_rq()
    #     report_rs = qb.send_xml(report_query_xml)
    #     print(report_rs)

    # def test_get_detail_report_file_open(self):
    #     """
    #     Only run this test if a company file is open.
    #     """
    #     qb = QuickbooksDesktop()
    #     report_query = CustomDetailReport.Query()
    #     report_query.report_date_macro = 'ThisYear'
    #     # report_query.include_column = []
    #     report_query_xml = report_query.to_xml()
    #     report_rs = qb.send_xml(report_query_xml)
    #     print(report_rs)

# class TestXMLParsing(unittest.TestCase):
#     def test_parse_field_according_to_type(self):
#         init_args = {}
#
#         col_desc_fields = {field.metadata["name"]: field for field in fields(ColDesc)}
#         test_field = col_desc_fields["ColTitle"]  # Retrieve the correct field
#         field_type = FromXmlMixin._get_field_type(test_field)  # Get the proper field type
#
#         xml_element = et.fromstring('<ColTitle>Title 1</ColTitle>')
#
#         init_args = FromXmlMixin._parse_field_according_to_type(init_args, test_field, field_type, xml_element)
#
#         self.assertEqual(init_args["col_title"], ["Title 1"])  # Expected output
