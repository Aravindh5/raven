
import logging
import config
import time
import datetime
from mysql_api import MysqlApi
import version
from argument_parser import ArgumentParser
from log_handler import LogHandler
from academy_model import AcademyModel, academy_db
from academy_schema import AcademyDataSchema, AcademyData, AcademyModelSchema
import requests
import json
import sys
from stats import Stats

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(config.LOG_ALIAS)
class ProcessData(object):
    def __init__(self, time_start=None, time_stop=None, incremental=None, dsa_url=None, dsa_oauth=None, academy_mysql_uri=None):
        logger.info('Starting ProcessData ..')
        self.start_time = time.time()
        self.academy_mysql_uri = academy_mysql_uri if academy_mysql_uri is not None else config.MYSQL_CONN['academy_mysql_uri']
        self.time_start = time_start if time_start is not None else config.REST_END_POINT['time_start']
        self.time_stop = time_stop if time_stop is not None else config.REST_END_POINT['time_stop']
        self.incremental = incremental if incremental is not None else config.REST_END_POINT['incremental']
        self.dsa_oauth = dsa_oauth if dsa_oauth is not None else config.REST_END_POINT['dsa_oauth']
        self.dsa_url = dsa_url if dsa_url is not None else config.REST_END_POINT['dsa_url']
        self.stats = Stats()

    def __del__(self):

        logger.info(self.stats.string())
        end_time = time.time()
        exec_time = end_time - self.start_time
        logger.info('Total time to run: {exec_hr:.0f} H, {exec_min:.0f} M, {exec_sec:.4f} S'.format(exec_hr=(exec_time/60)/60, exec_min=exec_time/60, exec_sec=exec_time))

    def start(self):
        logger.info('start()')
        self.create_mysql_conn();
        academy_data_list = []

        if(self.incremental):
            self.time_start = self.date_to_str(self.find_last_ticket_processed_date())
            self.time_stop = self.date_to_str(datetime.datetime.now())
            start = self.str_to_datetime(self.time_start) - datetime.timedelta(days=1)
            end = self.str_to_datetime(self.time_stop)
            # logger.info('Processing data for every 30 days from start date')
            while start < end:
                ins_start = start
                ins_end = start + datetime.timedelta(days=30)
                start = ins_end
                if ins_end > end:
                    ins_end = end
                academy_data_list = self.get_academy_data(self.date_to_str(ins_start), self.date_to_str(ins_end))
                if (academy_data_list is not None):
                    self.process_academy_data_list(academy_data_list)

        elif(self.time_start is not None  and self.time_stop is not None):
            start = self.str_to_datetime(self.time_start) - datetime.timedelta(days=1)
            end = self.str_to_datetime(self.time_stop)
            # logger.info('Processing data for every 30 days from start date')
            while start < end:
                ins_start = start
                ins_end = start + datetime.timedelta(days=30)
                start = ins_end
                if ins_end > end:
                    ins_end = end
                academy_data_list = self.get_academy_data(self.date_to_str(ins_start), self.date_to_str(ins_end))
                if(academy_data_list is not None):
                    self.process_academy_data_list(academy_data_list)

    def create_mysql_conn(self):
        # Initialize MYSQL Connection
        mysql_api = MysqlApi()
        mysql_api.init_academy_service(self.academy_mysql_uri)
        assert (mysql_api is not None)

    def get_academy_data(self, time_start, time_stop):
        logger.info(' time_start: {time_start}, time_stop: {time_stop}'.format(time_start=time_start, time_stop=time_stop))
        payload = {}
        payload['timestart'] = self.date_to_epoch(time_start);
        payload['timestop'] = self.date_to_epoch(time_stop);
        data = json.dumps(payload)

        headers = {}
        headers['content-type'] =  "application/json";
        headers['authorization'] =  self.dsa_oauth;
        try:
            response = requests.request("POST", self.dsa_url, data=data, headers=headers)
        except Exception as e:
            logger.error('There is an issue in Academy RestService. Check for right oauth or Raise concern to DSA - {reason}'.format(reason=e))
            raise ValueError('There is an issue in Academy RestService. Check for right oauth or Raise concern to DSA', e)

        if response.status_code == 200:
            academy_list = json.loads(response.content)
            if (len(academy_list) == 1 and "status" in academy_list):
                logger.info('Status: {status}'.format(status = academy_list['status'] ))
                return None
            else:
                return academy_list
        elif response.status_code == 500:
            logger.error('There is an issue in Academy RestService. Check for right oauth or Please raise concern to DSA  - {reason}'.format(reason=response.reason))
            raise ValueError('There is an issue in Academy RestService. Check for right oauth or Please raise concern to DSA', response.reason)

    def date_to_epoch(self, date):
        return str(int(time.mktime(time.strptime(date, "%Y-%m-%d"))))

    def date_to_str(self, dt, format='%Y-%m-%d'):
        return dt.strftime(format)

    def datetime_to_str(self, dt, format='%Y-%m-%d %H:%M:%S'):
        return datetime.date.strftime(dt, format)

    def str_to_datetime(self, dt, format='%Y-%m-%d'):
        return datetime.datetime.strptime(dt, format)

    def process_academy_data_list(self, academy_data_list):
        commits_count = 0
        academy_model_data_list = []
        for academy_data in academy_data_list:
            try:
                data = self._academy_validate_data(academy_data)
                academy_model_data = self._create_academy_model_data(data)
                    # MysqlApi.update_data(academy_model_data)
                # responce = MysqlApi.upsert_acamedy_data(academy_model_data)
                # if responce > 0:
                #     self.stats.success += 1
                # else:
                #     self.stats.errored += 1
                academy_model_data_list.append(academy_model_data)
                commits_count += 1
                self.stats.success += 1
                if (commits_count == config.MYSQL_COMMIT_EVERY):
                    logger.info(
                        'commits_count is: {commits_count}. Will commit to db now.'.format(commits_count=commits_count))
                    MysqlApi.upsert_acamedy_data(academy_model_data_list)
                    academy_model_data_list = []
                    commits_count = 0

            except Exception as e:
                self.stats.errored += 1
                logger.error('Error Processing data {msg}'.format(msg=e.message))

        if len(academy_model_data_list) > 0:
            MysqlApi.upsert_acamedy_data(academy_model_data_list)


    def _academy_validate_data(self, academy_data):
        # logger.info('_academy_validate_data()')
        data = None
        academy_data_schema =  AcademyDataSchema()
        data, errors = academy_data_schema.load(academy_data)
        if len(errors):
            logger.error('Error(s) while validating - user_id: {user_id} - user_id: {course_id}\n{errors}'.format(user_id = academy_data['uid'] , course_id=academy_data['nid'], errors=errors))
        else:
            return data


    def _create_academy_model_data(self, data):
        # logger.info('_create_gcal_event()')
        academy_model_data, errors = AcademyData._create_academy_model_data(data)

        if len(errors) > 0:
            logger.error('Error creating Academy model data: {errors}'.format(errors=errors))
        else:
            return academy_model_data


    def find_last_ticket_processed_date(self):
        return MysqlApi.find_max(AcademyModel.dsa_last_updated_ts);



def main():
    print ('Running version: {ver}'.format(ver=version.__version__))

    level, time_start, time_stop, incremental, dsa_url, dsa_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ArgumentParser().start()

    if level is not None:
        LogHandler(log_level=level)
    else:
        LogHandler()

    process_data = ProcessData(time_start=time_start, time_stop=time_stop, incremental=incremental,
                               dsa_url=dsa_url, dsa_oauth=dsa_oauth, academy_mysql_uri=academy_mysql_uri)

    # Debugs
    attr = vars(process_data)
    logger.info('\nPROGRAM PARAMETERS\n')
    logger.info(''.join('%s: %s\n' % item for item in attr.items()))

    process_data.start()


if __name__ == '__main__':
    main()