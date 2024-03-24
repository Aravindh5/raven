import unittest
import sys
import os
sys.path.append("../")

from raven.argument_parser import ArgumentParser

class TestArgumentParser(unittest.TestCase):
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

    def test_args_level(self):
        ap = ArgumentParser()
        test_level = 'DEBUG'
        sys.argv = ['prog', '--level', test_level]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, test_level, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_time_start(self):
        ap = ArgumentParser()
        test_time_start = '2017-01-01'
        sys.argv = ['prog', '--time_start', test_time_start]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, test_time_start, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_time_stop(self):
        ap = ArgumentParser()
        test_time_stop = '2017-01-01'
        sys.argv = ['prog', '--time_stop', test_time_stop]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, test_time_stop, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_incremental_for_production(self):
        ap = ArgumentParser()
        test_incremental = 'True'
        sys.argv = ['prog', '--incremental', test_incremental]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, True, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_incremental_for_developement(self):
        ap = ArgumentParser()
        test_incremental = 'False'
        sys.argv = ['prog', '--incremental', test_incremental]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, False, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')
    #
    def test_args_dsa_url(self):
        ap = ArgumentParser()
        test_dsa_url = 'https://dsaweb-31-datastax-academy.pantheonsite.io/c360/updateC360/index.json'
        sys.argv = ['prog', '--dsa_url', test_dsa_url]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, test_dsa_url, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_dsa_oauth(self):
        ap = ArgumentParser()
        test_dsa_oauth = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYWNhZGVteS5kYXRhc3RheC5jb20iLCJhdWQiOiJodHRwczpcL1wvYWNhZGVteS5kYXRhc3RheC5jb20iLCJqdGkiOiJpblg3YnQ1Q3U1Zy1vUk9MaTdpdEY0bEMtRV9iUk94akJNbG8tWFJDcUdZIiwiZXhwIjoxNTE4ODIyMDc5LCJuYmYiOjE1MTYyMzAwNzksImlhdCI6MTUxNjIzMDA3OSwiZW1haWwiOiJzeXNhZG1pbkBkYXRhc3RheC5jb20iLCJzdWIiOiI3NTgxY2FlOS0yMWZlLTQ4MWEtOTg4Zi01NzEzMWQwOTNkMjUifQ.aRrvAfXLcpx0VTv81eAGyhUEkNhUSLS4EQWLiFz9IMI'
        sys.argv = ['prog', '--dsa_oauth', test_dsa_oauth]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, test_dsa_oauth, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_c360_mysql_uri(self):
        ap = ArgumentParser()
        test_c360_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        sys.argv = ['prog', '--c360_mysql_uri', test_c360_mysql_uri]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, test_c360_mysql_uri, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_for_sfdc_mysql_uri(self):
        ap = ArgumentParser()
        test_sfdc_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        sys.argv = ['prog', '--sfdc_mysql_uri', test_sfdc_mysql_uri]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, test_sfdc_mysql_uri, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_for_academy_mysql_uri(self):
        ap = ArgumentParser()
        test_academy_mysql_uri = 'mysql://root:aravindh@127.0.0.1/mysql'
        sys.argv = ['prog', '--academy_mysql_uri', test_academy_mysql_uri]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, test_academy_mysql_uri, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, None, 'Argument data_dir is not being parsed correctly')

    def test_args_for_data_dir(self):
        ap = ArgumentParser()
        test_data_dir = '/home/PycharmProjects/raven/python/data'
        sys.argv = ['prog', '--data_dir', test_data_dir]
        level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ap.start()
        self.assertEqual(level, None, 'Argument level is not being parsed correctly')
        self.assertEqual(time_start, None, 'Argument time_start is not being parsed correctly')
        self.assertEqual(time_stop, None, 'Argument timestop is not being parsed correctly')
        self.assertEqual(incremental, None, 'Argument incremental is not being parsed correctly')
        self.assertEqual(dsa_url, None, 'Argument dsa_url is not being parsed correctly')
        self.assertEqual(dsa_oauth, None, 'Argument dsa_oauth is not being parsed correctly')
        self.assertEqual(c360_mysql_uri, None, 'Argument c360_mysql_uri is not being parsed correctly')
        self.assertEqual(sfdc_mysql_uri, None, 'Argument sfdc_mysql_uri is not being parsed correctly')
        self.assertEqual(academy_mysql_uri, None, 'Argument academy_mysql_uri is not being parsed correctly')
        self.assertEqual(data_dir, test_data_dir, 'Argument data_dir is not being parsed correctly')

suite = unittest.TestLoader().loadTestsFromTestCase(TestArgumentParser)
unittest.TextTestRunner(verbosity=2).run(suite)