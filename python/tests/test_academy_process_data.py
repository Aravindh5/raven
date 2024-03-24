__author__ = 'Valtanix Inc.,'

import datetime
import sys
import unittest
import os.path
sys.path.append("../")

from nose.tools import *
from raven.academy_process_data import ProcessData


class TestProcessingData(unittest.TestCase):


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

    def test_mysql_connection(self):
        process = ProcessData()
        connection = process.create_mysql_conn()
        self.assertEqual(connection, None)

    def test_date_to_epoch(self):
        process = ProcessData()
        epoch = process.date_to_epoch('2017-03-20')
        self.assertAlmostEqual('1489948200', epoch)

    def test_date_to_str(self):
        process = ProcessData()
        date = process.date_to_str(datetime.datetime(2017, 12, 30, 0, 0))
        self.assertTrue(type(date) is str)

    def test_converting_string_to_date(self):
        process = ProcessData()
        date = process.str_to_datetime('2017-12-30')
        self.assertEqual(date, datetime.datetime(2017, 12, 30, 0, 0))

    def test_converting_datetime_to_string(self):
        process = ProcessData()
        date = process.datetime_to_str(datetime.datetime(2017, 12, 30, 0, 0))
        self.assertEqual(date, '2017-12-30 00:00:00')

    def test_get_academy_data(self):
        process = ProcessData()
        academy_list = process.get_academy_data('2017-03-20', '2018-12-21')
        self.assertTrue(type(academy_list) is list)

    def test_getting_illegal_data(self):
        process = ProcessData()
        data = process.get_academy_data('2018-02-01', '2017-01-01')
        self.assertFalse(type(data) is list)

    def test_academy_valid_data(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started':
                            '1513135727', 'nid': '6102', 'finished': '0',
                        'progress': '86', 'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertTrue(type(data) is dict)

    def test_academy_invalid_data_without_updated_time(self):
        academy_data = {'updated': None, 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started':
                            '1513135727', 'nid': '6102', 'finished': '0',
                        'progress': '86', 'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_uid_with_null(self):
        academy_data = {'updated': '1513760409', 'uid': None,
                        'title': 'DS220: Data Modeling', 'started': '1513135727',
                        'nid': '6102', 'finished': '0', 'progress': '86',
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_tilte_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': None, 'started': '1513135727',
                        'nid': '6102', 'finished': '0', 'progress': '86',
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_started_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started': None,
                        'nid': '6102', 'finished': '0', 'progress': '86',
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_nid_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started': '1513135727',
                        'nid': None, 'finished': '0', 'progress': '86',
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_finished_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started': '1513135727',
                        'nid': '6102', 'finished': None, 'progress': '86',
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_academy_invalid_data_progress_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling',
                        'started': '1513135727', 'nid': '6102',
                        'finished': '0', 'progress': None,
                        'email': '1120861386@qq.com'}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    # email should not be null
    def test_academy_invalid_data_email_as_null(self):
        academy_data = {'updated': '1513760409', 'uid': '137879',
                        'title': 'DS220: Data Modeling', 'started': '1513135727',
                        'nid': '6102', 'finished': '0', 'progress': '0',
                        'email': None}
        process = ProcessData()
        data = process._academy_validate_data(academy_data)
        self.assertFalse(type(data) is dict)

    def test_creating_academy_model(self):
        data = {'updated': 1513760409, 'uid': 137879,
                'start_ts_extract': datetime.datetime(2017, 12, 13, 8, 58, 47),
                'title': 'DS220: Data Modeling', 'started': 1513135727,
                'nid': 6102, 'finished': 0, 'email_extract': '1120861386@qq.com',
                'finish_ts_extract': None, 'progress': 86,
                'dsa_last_updated_ts_extract': datetime.datetime(2017, 12, 20, 14, 30, 9),
                'email': '1120861386@qq.com'}
        process = ProcessData()
        academy_model = process._create_academy_model_data(data)
        self.assertTrue(type(academy_model) is dict)

    def test_creating_academy_model_for_invalid_data(self):
        data = {'updated': 1513760409, 'uid': 137879,
                'start_ts_extract': datetime.datetime(2017, 12, 13, 8, 58, 47),
                'title': 'DS220: Data Modeling', 'started': 1513135727, 'nid': 6102,
                'finished': 0, 'email_extract': '1120861386@qq.com',
                'finish_ts_extract': None, 'progress': 86,
                'dsa_last_updated_ts_extract': datetime.datetime(2017, 12, 20, 14, 30, 9),
                'email': '1120861386@qq.com'}
        process = ProcessData()
        academy_model = process._create_academy_model_data(data)
        self.assertTrue(type(academy_model) is dict)

    def test_creating_academy_model_data_with_null_values(self):
        process = ProcessData()
        data = {'uid': None, 'nid': None, 'title': None, 'email_extract': None,
                'start_ts_extract': None, 'finish_ts_extract': None,
                'dsa_last_updated_ts_extract': None, 'progress': None}
        academy_model = process._create_academy_model_data(data)
        self.assertTrue(type(academy_model) is dict)

    def test_process_academy_data_list(self):
        academy_data_list = [{'updated': '1513760409', 'uid': '137879',
                              'title': 'DS220: Data Modeling',
                              'started': '1513135727', 'nid': '6102',
                              'finished': '0', 'progress': '86',
                              'email': '1120861386@qq.com'},
                             {'updated': '1514760409', 'uid': '147879',
                              'title': 'DS230: Data Haandling',
                              'started': '1613135727', 'nid': '6103',
                              'finished': '10', 'progress': '89',
                              'email': 'ktaravindh005@gmail.com'}, ]
        process = ProcessData()
        data = process.process_academy_data_list(academy_data_list)
        self.assertEqual(data, None)

    def test_process_academy_data_list_with_more_than_50_data(self):
        academy_data_list = [
                            {
                                "updated": "1513760409",
                                "email": "1120861386@qq.com",
                                "uid": "137879",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1513135727",
                                "finished": "0",
                                "progress": "86"
                            },
                            {
                                "updated": "1514278769",
                                "email": "1159247360@qq.com",
                                "uid": "138694",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1514278769",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1513971911",
                                "email": "157rahul@gmail.com",
                                "uid": "138602",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513971911",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515723842",
                                "email": "16866366@qq.com",
                                "uid": "139814",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1515723842",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515654910",
                                "email": "24.sachin@gmail.com",
                                "uid": "135096",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1511163381",
                                "finished": "0",
                                "progress": "16"
                            },
                            {
                                "updated": "1514141165",
                                "email": "2ranjan.gupta@gmail.com",
                                "uid": "133419",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1514141165",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514150664",
                                "email": "2ranjan.gupta@gmail.com",
                                "uid": "133419",
                                "nid": "6193",
                                "title": "DS330: DataStax Enterprise Graph",
                                "started": "1508339030",
                                "finished": "0",
                                "progress": "14"
                            },
                            {
                                "updated": "1515388004",
                                "email": "2reachvenkat@gmail.com",
                                "uid": "134893",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1511138337",
                                "finished": "0",
                                "progress": "92"
                            },
                            {
                                "updated": "1514871986",
                                "email": "2reachvenkat@gmail.com",
                                "uid": "134893",
                                "nid": "6052",
                                "title": "DS210: DataStax Enterprise Operations with Apache Cassandra",
                                "started": "1511151961",
                                "finished": "0",
                                "progress": "3"
                            },
                            {
                                "updated": "1514749990",
                                "email": "2reachvenkat@gmail.com",
                                "uid": "134893",
                                "nid": "6122",
                                "title": "DS310: DataStax Enterprise Search",
                                "started": "1514749990",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1513892686",
                                "email": "44gphillips@googlemail.com",
                                "uid": "138546",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513890950",
                                "finished": "0",
                                "progress": "67"
                            },
                            {
                                "updated": "1513846393",
                                "email": "4sathya@gmail.com",
                                "uid": "104993",
                                "nid": "2097",
                                "title": "A Brief Introduction to Apache Cassandra",
                                "started": "1513846393",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515601281",
                                "email": "513228837@qq.com",
                                "uid": "139458",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1515428989",
                                "finished": "0",
                                "progress": "2"
                            },
                            {
                                "updated": "1514689515",
                                "email": "7777benjib@gmail.com",
                                "uid": "136444",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1511795643",
                                "finished": "0",
                                "progress": "48"
                            },
                            {
                                "updated": "1514172872",
                                "email": "877142411@qq.com",
                                "uid": "138663",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1514172872",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514916316",
                                "email": "89neuron@gmail.com",
                                "uid": "139052",
                                "nid": "6193",
                                "title": "DS330: DataStax Enterprise Graph",
                                "started": "1514916316",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514916378",
                                "email": "89neuron@gmail.com",
                                "uid": "139052",
                                "nid": "2239",
                                "title": "Getting Started with TinkerPop and Gremlin",
                                "started": "1514916378",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514125100",
                                "email": "a.hosseini.68@gmail.com",
                                "uid": "134953",
                                "nid": "2218",
                                "title": "Getting Started with Apache Spark and Cassandra",
                                "started": "1514125100",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515672374",
                                "email": "a.macey@tmd-associates.co.uk",
                                "uid": "20275",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1515672374",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514165414",
                                "email": "a.obeidat@t2.sa",
                                "uid": "138661",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1514165414",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514168693",
                                "email": "a.obeidat@t2.sa",
                                "uid": "138661",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1514168118",
                                "finished": "0",
                                "progress": "10"
                            },
                            {
                                "updated": "1514127838",
                                "email": "a.shkarupin@gmail.com",
                                "uid": "138649",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1514124529",
                                "finished": "1514127838",
                                "progress": "100"
                            },
                            {
                                "updated": "1514809235",
                                "email": "a.shkarupin@gmail.com",
                                "uid": "138649",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1514293565",
                                "finished": "1514809235",
                                "progress": "100"
                            },
                            {
                                "updated": "1514225748",
                                "email": "a.shkarupin@gmail.com",
                                "uid": "138649",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1514128420",
                                "finished": "1514225748",
                                "progress": "100"
                            },
                            {
                                "updated": "1515097067",
                                "email": "a588635@fmr.com",
                                "uid": "103345",
                                "nid": "6122",
                                "title": "DS310: DataStax Enterprise Search",
                                "started": "1515094380",
                                "finished": "0",
                                "progress": "21"
                            },
                            {
                                "updated": "1514285872",
                                "email": "aa00365757@techmahindra.com",
                                "uid": "138711",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1514285872",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514285903",
                                "email": "aa00365757@techmahindra.com",
                                "uid": "138711",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1514285903",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514419977",
                                "email": "aaan.br@hotmail.com",
                                "uid": "101626",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1485824362",
                                "finished": "0",
                                "progress": "10"
                            },
                            {
                                "updated": "1513770200",
                                "email": "aakarshi92@gmail.com",
                                "uid": "138332",
                                "nid": "1985",
                                "title": "Getting Started with Apache Cassandra and Python",
                                "started": "1513768364",
                                "finished": "0",
                                "progress": "67"
                            },
                            {
                                "updated": "1513749384",
                                "email": "aakarshi92@gmail.com",
                                "uid": "138332",
                                "nid": "6052",
                                "title": "DS210: DataStax Enterprise Operations with Apache Cassandra",
                                "started": "1513749384",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1513882824",
                                "email": "aaldridge@alexinc.com",
                                "uid": "127563",
                                "nid": "1985",
                                "title": "Getting Started with Apache Cassandra and Python",
                                "started": "1513874287",
                                "finished": "0",
                                "progress": "67"
                            },
                            {
                                "updated": "1513887585",
                                "email": "aaldridge@alexinc.com",
                                "uid": "127563",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1513887585",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515449946",
                                "email": "aandradeblazquez@gmail.com",
                                "uid": "137611",
                                "nid": "1985",
                                "title": "Getting Started with Apache Cassandra and Python",
                                "started": "1515264873",
                                "finished": "0",
                                "progress": "33"
                            },
                            {
                                "updated": "1514897967",
                                "email": "aandradeblazquez@gmail.com",
                                "uid": "137611",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1512836736",
                                "finished": "0",
                                "progress": "39"
                            },
                            {
                                "updated": "1514879903",
                                "email": "aandresruiz91@gmail.com",
                                "uid": "138037",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1513610934",
                                "finished": "0",
                                "progress": "14"
                            },
                            {
                                "updated": "1513758967",
                                "email": "aandresruiz91@gmail.com",
                                "uid": "138037",
                                "nid": "2813",
                                "title": "Getting started with KillrVideo: An Example Playlist "
                                         "and Recommendation Engine Application",
                                "started": "1513758967",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514975688",
                                "email": "aaradhaa@googlemail.com",
                                "uid": "117045",
                                "nid": "6018",
                                "title": "DS201: DataStax Enterprise Foundations of Apache Cassandra",
                                "started": "1495048425",
                                "finished": "0",
                                "progress": "5"
                            },
                            {
                                "updated": "1515364016",
                                "email": "aaronbalaster@gmail.com",
                                "uid": "139079",
                                "nid": "2193",
                                "title": "Getting Started with Time Series Data Modeling",
                                "started": "1515364016",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515365490",
                                "email": "aaronbalaster@gmail.com",
                                "uid": "139079",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1515365490",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514352593",
                                "email": "abaghumian@noggin.com.au",
                                "uid": "136315",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1511415690",
                                "finished": "0",
                                "progress": "86"
                            },
                            {
                                "updated": "1513887703",
                                "email": "abd786.ap@gmail.com",
                                "uid": "114331",
                                "nid": "6264",
                                "title": "[Legacy - Cassandra 2.x ] DS201: Cassandra Core Concepts ",
                                "started": "1504374144",
                                "finished": "0",
                                "progress": "16"
                            },
                            {
                                "updated": "1514166283",
                                "email": "abdgadry@gmail.com",
                                "uid": "136449",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1513822800",
                                "finished": "1514166283",
                                "progress": "100"
                            },
                            {
                                "updated": "1513822656",
                                "email": "abdgadry@gmail.com",
                                "uid": "136449",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513803261",
                                "finished": "1513822656",
                                "progress": "100"
                            },
                            {
                                "updated": "1514240492",
                                "email": "abdgadry@gmail.com",
                                "uid": "136449",
                                "nid": "6170",
                                "title": "DS320: DataStax Enterprise Analytics with Apache Spark",
                                "started": "1514166367",
                                "finished": "1514240492",
                                "progress": "100"
                            },
                            {
                                "updated": "1513943949",
                                "email": "abdul.m.qadeer@verizon.com",
                                "uid": "128611",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513943949",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1513861697",
                                "email": "abeumer@quintor.nl",
                                "uid": "138365",
                                "nid": "6102",
                                "title": "DS220: Data Modeling",
                                "started": "1513776186",
                                "finished": "0",
                                "progress": "22"
                            },
                            {
                                "updated": "1513776531",
                                "email": "abeumer@quintor.nl",
                                "uid": "138365",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513697169",
                                "finished": "1513776531",
                                "progress": "100"
                            },
                            {
                                "updated": "1513793805",
                                "email": "abhay_nirgudkar@ml.com",
                                "uid": "94712",
                                "nid": "5996",
                                "title": "DS101: Introduction to Apache Cassandra",
                                "started": "1513793805",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515395297",
                                "email": "abhi2kk@gmail.com",
                                "uid": "137679",
                                "nid": "2218",
                                "title": "Getting Started with Apache Spark and Cassandra",
                                "started": "1515395297",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1515005300",
                                "email": "Abhijeetgupta29nov@gmail.com",
                                "uid": "138967",
                                "nid": "2097",
                                "title": "A Brief Introduction to Apache Cassandra",
                                "started": "1515005300",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514799496",
                                "email": "ABHISHEK.KAUSHAL@YMAIL.COM",
                                "uid": "138979",
                                "nid": "6052",
                                "title": "DS210: DataStax Enterprise Operations with Apache Cassandra",
                                "started": "1514799496",
                                "finished": "0",
                                "progress": "0"
                            },
                            {
                                "updated": "1514874057",
                                "email": "ABHISHEK.KAUSHAL@YMAIL.COM",
                                "uid": "138979",
                                "nid": "1985",
                                "title": "Getting Started with Apache Cassandra and Python",
                                "started": "1514874057",
                                "finished": '0',
                                "progress": "0"
                            },
                            {
                                "updated": "1514262641",
                                "email": "anirudh2.gupta@aricent.com",
                                "uid": "138566",
                                "nid": "5732",
                                "title": "Download & Install DataStax Enterprise",
                                "started": "1514262641",
                                "finished": "0",
                                "progress": "0"
                            }
                            ]
        process = ProcessData()
        data = process.process_academy_data_list(academy_data_list)
        self.assertEqual(data, None)


suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessingData)
unittest.TextTestRunner(verbosity=2).run(suite)
