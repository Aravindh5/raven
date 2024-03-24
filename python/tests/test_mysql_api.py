import unittest
import sys
sys.path.append("../")

from raven.mysql_api import MysqlApi


class TestMySqlApi(unittest.TestCase):

    def test_init_academy_service(self):
        mysql_uri = 'mysql://c360:Stax123@54.67.36.103/dsa'
        mysql = MysqlApi()
        conn = mysql.init_academy_service(mysql_uri)
        assert conn is None

    def test_init_lead_service(self):
        mysql_uri = 'mysql://c360:Stax123@54.67.36.103/Sdexport'
        mysql = MysqlApi()
        conn = mysql.init_lead_service(mysql_uri)
        assert conn is None

    def test_init_contact_service(self):
        mysql_uri = 'mysql://c360:Stax123@54.67.36.103/Sdexport'
        mysql = MysqlApi()
        conn = mysql.init_contact_service(mysql_uri)
        assert conn is None

    def test_init_account_service(self):
        mysql_uri = 'mysql://c360:Stax123@54.67.36.103/c360_dev'
        mysql = MysqlApi()
        conn = mysql.init_account_service(mysql_uri)
        assert conn is None


suite = unittest.TestLoader().loadTestsFromTestCase(TestMySqlApi)
unittest.TextTestRunner(verbosity=2).run(suite)
