import logging
import tldextract
import config
import time
import numpy as np
import pandas as pd
from mysql_api import MysqlApi
import version
from argument_parser import ArgumentParser
from log_handler import LogHandler
import sys
from stats import Stats
import os

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(config.LOG_ALIAS)


class ProcessData(object):
    def __init__(self, c360_mysql_uri=None, sfdc_mysql_uri=None, academy_mysql_uri=None, data_dir=None):
        logger.info('Starting ProcessData ..')
        self.start_time = time.time()
        self.academy_mysql_uri = academy_mysql_uri if academy_mysql_uri is not None else config.MYSQL_CONN['academy_mysql_uri']
        self.sfdc_mysql_uri = sfdc_mysql_uri if sfdc_mysql_uri is not None else config.MYSQL_CONN['sfdc_mysql_uri']
        self.c360_mysql_uri = c360_mysql_uri if c360_mysql_uri is not None else config.MYSQL_CONN['c360_mysql_uri']
        self.data_dir = data_dir if data_dir is not None else config.DATA_DIR
        self.free_email_proviers_file_name = self.data_dir + os.sep + config.FREE_EMAIL_PROVIDERS

        # Data directory existence check
        if os.path.isdir(self.data_dir) is False:
            logger.info('Data Directory {data_dir} must exist!'.format(data_dir =self.data_dir))
            sys.exit(-1)

        # Free email providers existence check
        if os.path.isfile(self.free_email_proviers_file_name ) is False:
            logger.info('File {free_service_providers_file} must exist!'.format(free_service_providers_file=self.free_email_proviers_file_name ))
            sys.exit(-1)

        self.free_service_providers_df = pd.read_csv(self.free_email_proviers_file_name )

        self.stats = Stats()

    def __del__(self):
        logger.info(self.stats.string())
        end_time = time.time()
        exec_time = end_time - self.start_time
        logger.info('Total time to run: {exec_hr:.0f} H, {exec_min:.0f} M, {exec_sec:.4f} S'.format(
            exec_hr=(exec_time / 60) / 60, exec_min=exec_time / 60, exec_sec=exec_time))

    def start(self):
        self.create_mysql_conn()
        self.academy_list = MysqlApi.get_all_academy()
        self.lead_dict = MysqlApi.get_all_leads()
        self.contact_dict = MysqlApi.get_all_contacts()
        self.account_df = MysqlApi.get_all_accounts()

        self.local_email_dict = {}

        commits_count = 0
        count = 0
        academy_data_list = []
        for academy_model in self.academy_list:
            count += 1
            if count%100==0:
                logger.info('processed_count: {commits_count}.'.format(commits_count=count))

            try:
                sfdc_id = None
                role = None
                email = academy_model['email']

                try:
                    result_df = self.local_email_dict[email]
                except:
                    result_df = None

                if result_df is not None:
                    sfdc_id = result_df['sfdc_id']
                    role = result_df['role']
                else:
                    sfdc_id, role = self.find_sfdc_data(academy_model)
                    if sfdc_id is not None:
                        temp_dict = {'sfdc_id': sfdc_id, 'role': role}
                        self.local_email_dict[email] = temp_dict

                if sfdc_id is not None:
                    if (sfdc_id != academy_model['sfdc_id'] or role != academy_model['role']):
                        academy_model['sfdc_id']=sfdc_id
                        academy_model['role']=role
                        academy_data_list.append(self.map_sfdc_data(academy_model))
                        commits_count += 1
                        self.stats.success += 1

                        if (commits_count == config.MYSQL_COMMIT_EVERY):
                            logger.info('commits_count: {commits_count}. Will commit to db now.'.format(
                                    commits_count=commits_count))

                            MysqlApi.bulk_update_data(academy_data_list)
                            academy_data_list = []
                            commits_count = 0
                    else:
                        # logger.info('{email} is already up-to-date {sfdc_id}'.format(email=academy_model.email, sfdc_id=academy_model.sfdc_id))
                        self.stats.success += 1
                else:
                    self.stats.skipped += 1
            except Exception as e:
                self.stats.errored += 1
                logger.error('Error Processing data {msg}'.format(msg=e.message))

        if len(academy_data_list) > 0:
            MysqlApi.bulk_update_data(academy_data_list)

    def map_sfdc_data(self, academy_model):
        aca_dict = {}
        aca_dict['sfdc_id'] = academy_model['sfdc_id']
        aca_dict['role'] = academy_model['role']
        aca_dict['course_id'] = academy_model['course_id']
        aca_dict['user_id'] = academy_model['user_id']
        return aca_dict

    def find_sfdc_data(self, academy_model):
        sfdc_id = None
        role = None
        email = academy_model['email']
        if (academy_model is not None):
            try:
                result_df = self.lead_dict[email]
            except:
                result_df = None
            if result_df is not None:
                # logger.info('Data found in Lead table')
                sfdc_id = result_df['sfdc_id']
                role = result_df['role']
                return sfdc_id, role

            try:
                result_df = self.contact_dict[email]
            except:
                result_df = None
            if result_df is not None:
                # logger.info('Data found in Contact table')
                sfdc_id = result_df['sfdc_id']
                role = result_df['role']
                return sfdc_id, role

            domain = email.split("@")[1]
            # logger.info(domain)
            is_free_service_df = self.free_service_providers_df[self.free_service_providers_df.domain == domain]
            if len(is_free_service_df) == 0:
                result_df = self.account_df[self.account_df['website'].str.contains(domain, na=False)]
                #Get the domain value
                if len(result_df.index) == 1:
                    # logger.info('Data found in Account table')
                    val = result_df.iloc[0]['sfdc_id']
                    if val is not np.nan:
                        sfdc_id = val
                    return sfdc_id, role
                elif len(result_df.index) > 1:
                    # logger.info('Data found in Account table')
                    #Find the exact domain match, if more then one domain get filtered
                    for web_index, web in result_df.iterrows():
                        domail_list = tldextract.extract(web['website'])
                        domain_name = domail_list.domain + '.' + domail_list.suffix
                        if domain_name == domain:
                            val = web['sfdc_id']
                            if val is not np.nan:
                                sfdc_id = val
                            return sfdc_id, role

            # else:
                # logger.info("{domain} is free service provider".format(domain=domain))
            return None, None

    def create_mysql_conn(self):
        # Initialize MYSQL Connection
        academy_mysql_api = MysqlApi()
        academy_mysql_api.init_academy_service(self.academy_mysql_uri)
        assert (academy_mysql_api is not None)

        lead_mysql_api = MysqlApi()
        lead_mysql_api.init_lead_service(self.sfdc_mysql_uri)
        assert (lead_mysql_api is not None)

        contact_mysql_api = MysqlApi()
        contact_mysql_api.init_contact_service(self.sfdc_mysql_uri)
        assert (contact_mysql_api is not None)

        account_mysql_api = MysqlApi()
        account_mysql_api.init_account_service(self.c360_mysql_uri)
        assert (account_mysql_api is not None)


def main():
    print ('Running version: {ver}'.format(ver=version.__version__))

    level, time_start, time_stop, incremental, rest_url, rest_oauth, c360_mysql_uri, sfdc_mysql_uri, academy_mysql_uri, data_dir = ArgumentParser().start()

    if level is not None:
        LogHandler(log_level=level)
    else:
        LogHandler()

    process_data = ProcessData(c360_mysql_uri=c360_mysql_uri, sfdc_mysql_uri=sfdc_mysql_uri, academy_mysql_uri=academy_mysql_uri, data_dir=data_dir)

    # Debugs
    attr = vars(process_data)
    # logger.info('\nPROGRAM PARAMETERS\n')
    # logger.info(''.join('%s: %s\n' % item for item in attr.items()))

    process_data.start()

if __name__ == '__main__':
    main()