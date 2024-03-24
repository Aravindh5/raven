import unittest
import config
import pandas as pd
import os.path
import sys
sys.path.append("../")

from nose.tools import *
from raven.map_sfdc_process_data import ProcessData
from raven.mysql_api import MysqlApi


class TestSfdcProcessData(unittest.TestCase):

    @classmethod
    def setup_class(self):
        """This method is run once for each class before any tests are run"""
        print 'setup_class'

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""
        print 'teardown_class'

    def setUp(self):
        """This method is run once before _each_ test method is executed"""
        print 'setUp'

    def teardown(self):
        """This method is run once after _each_ test method is executed"""
        print 'teardown'


    def test_creating_mysql_connection(self):
        # process = ProcessData()
        # process.create_mysql_conn()

        mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        mysql_api = MysqlApi()
        mysql_api.init_academy_service(mysql_uri)
        assert (mysql_api is not None)

        zendesk_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        lead_mysql_api = MysqlApi()
        lead_mysql_api.init_lead_service(zendesk_mysql_uri)
        assert (lead_mysql_api is not None)

        zendesk_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        contact_mysql_api = MysqlApi()
        contact_mysql_api.init_contact_service(zendesk_mysql_uri)
        assert (contact_mysql_api is not None)

        c360_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        account_mysql_api = MysqlApi()
        account_mysql_api.init_account_service(c360_mysql_uri)
        assert (account_mysql_api is not None)

    def test_wrong_mysql_uri(self):
        # process = ProcessData()
        # process.create_mysql_conn()

        mysql_uri = 'invalid url'
        mysql_api = MysqlApi()
        mysql_api.init_academy_service(mysql_uri)
        self.assertIsNotNone(mysql_api)

        zendesk_mysql_uri = 'invalid url'
        lead_mysql_api = MysqlApi()
        lead_mysql_api.init_lead_service(zendesk_mysql_uri)
        self.assertIsNotNone(lead_mysql_api)

        zendesk_mysql_uri = 'invalid url'
        contact_mysql_api = MysqlApi()
        contact_mysql_api.init_contact_service(zendesk_mysql_uri)
        self.assertIsNotNone(contact_mysql_api)

        c360_mysql_uri = 'invalid url'
        account_mysql_api = MysqlApi()
        account_mysql_api.init_account_service(c360_mysql_uri)
        self.assertIsNotNone(account_mysql_api)

    def test_map_sfdc_process_data(self):
        process = ProcessData()
        academy_model = {'user_id': 1, 'course_id': 101, 'title': 'DS:101', 'email': 'ktaravindh005@gmail.com',
                         'last_updated_ts': '2018-02-16 18:46:24', 'start_ts': '2017-01-31 18:45:12',
                         'finish_ts': '2018-02-16 18:46:24', 'progress': '0',
                         'dsa_last_updated_ts': '2018-02-16 18:46:24',
                         'sfdc_id': '001aaabbbccc', 'role': 'Junior software developer'}
        result = process.map_sfdc_data(academy_model)
        self.assertTrue(type(result) is dict)

    def test_finding_sfdc_data_in_lead_table(self):
        academy_model = {"user_id": 1, "course_id": 101, "title": "DS:101", "email": "ktaravindh005@gmail.com",
                         "last_updated_ts": "2018-02-16 18:46:24", "start_ts": "2017-01-31 18:45:12",
                         "finish_ts": "2018-02-16 18:46:24", "progress": "0",
                         "dsa_last_updated_ts": "2018-02-16 18:46:24"}
        process = ProcessData()
        process.lead_dict = {"ktaravindh005@gmail.com": {"sfdc_id": "000111222", "role": "Software Engineer"}}
        sfdc_id, role = process.find_sfdc_data(academy_model)
        self.assertTrue(type(sfdc_id) is str)
        self.assertTrue(type(role) is str)

    def test_finding_sfdc_data_in_contact_table(self):
        academy_model = {"user_id": 4, "course_id": 104, "title": "DS:101", "email": "aakash@gmail.com",
                         "last_updated_ts": "2018-02-16 18:46:24", "start_ts": "2017-01-31 18:45:12",
                         "finish_ts": "2018-02-16 18:46:24", "progress": "0",
                         "dsa_last_updated_ts": "2018-02-16 18:46:24"}
        process = ProcessData()
        process.contact_dict = {"aakash@gmail.com": {"sfdc_id": "002aaabbbccc", "role": "Sales_force_developer"}}
        sfdc_id, role = process.find_sfdc_data(academy_model)
        self.assertTrue(type(sfdc_id) is str)
        self.assertTrue(type(role) is str)

    def test_finding_sfdc_data_in_account_table(self):
        academy_model = {"user_id": 5, "course_id": 105, "title": "DS:101", "email": "aravindh@valtanix.net",
                         "last_updated_ts": "2018-02-16 18:46:24", "start_ts": "2017-01-31 18:45:12",
                         "finish_ts": "2018-02-16 18:46:24", "progress": "0",
                         "dsa_last_updated_ts": "2018-02-16 18:46:24"}
        process = ProcessData()
        account_list = [{"website": "www.valtanix.net", "sfdc_id": "000111aaabbb"},
                        {"website": "www.oneindia.com", "sfdc_id": "11111111"}]
        process.account_df = pd.DataFrame(account_list)
        sfdc_id, role = process.find_sfdc_data(academy_model)
        self.assertTrue(type(sfdc_id) is str)
        self.assertIsNone(role)

    def test_finding_sfdc_data_in_account_table_with_same_kind_of_email(self):
        academy_model = {"user_id": 5, "course_id": 105, "title": "DS:101", "email": "aravindh@dog.net",
                         "last_updated_ts": "2018-02-16 18:46:24", "start_ts": "2017-01-31 18:45:12",
                         "finish_ts": "2018-02-16 18:46:24", "progress": "0",
                         "dsa_last_updated_ts": "2018-02-16 18:46:24"}
        process = ProcessData()
        account_list = [{"website": "www.one.dog.net", "sfdc_id": "000111aaabbb"},
                        {"website": "www.dog.net", "sfdc_id": "11111111"}]
        process.account_df = pd.DataFrame(account_list)
        sfdc_id, role = process.find_sfdc_data(academy_model)
        self.assertTrue(type(sfdc_id) is str)
        self.assertIsNone(role)

    def test_start(self):
        process = ProcessData()
        result = process.start()
        self.assertEqual(result, None)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSfdcProcessData)
unittest.TextTestRunner(verbosity=2).run(suite)
