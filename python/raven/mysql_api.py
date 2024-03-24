from flask import Flask
import logging
import config
from academy_model import academy_db, AcademyModel
from lead_model import lead_db, LeadModel
from contact_model import contact_db, ContactModel
from account_model import account_db, AccountModel
from sqlalchemy import func
import pandas as pd

logger = logging.getLogger(config.LOG_ALIAS)

class MysqlApi(object):


    def init_academy_service(self, mysql_uri):
        logger.info('Initilizating Mysql Connection ..')
        try:
            app = Flask(__name__)
            app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
            academy_db.app = app
            academy_db.init_app(app)
        except Exception as e:
            logger.error('Error Connecting to Mysql {msg}'.format(msg=e.message))
            raise

    @staticmethod
    def get_all_academy():
        logger.info('get_all_academy()')
        academy_list = []
        try:
            academy_model_list = AcademyModel.query.all()
            for ac in academy_model_list:
                temp_dict = {'email': ac.email.lower(), 'sfdc_id': ac.sfdc_id, 'role': ac.role, 'user_id': ac.user_id, 'course_id': ac.course_id}
                academy_list.append(temp_dict)
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise
        return academy_list

    def init_lead_service(self, mysql_uri):
        logger.info('Initilizating Mysql Connection ..')
        try:
            app = Flask(__name__)
            app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
            lead_db.app = app
            lead_db.init_app(app)
        except Exception as e:
            logger.error('Error Connecting to Mysql {msg}'.format(msg=e.message))
            raise

    @staticmethod
    def get_all_leads():
        logger.info('get_all_leads()')
        lead_dict = {}
        try:
            lead_model_list = LeadModel.query.filter((LeadModel.existing_account__c != None) | (LeadModel.convertedaccountid != None)).filter(LeadModel.email != None).all()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise
        for lead_model in lead_model_list:
            email = lead_model.email.lower()
            temp_dict = {'sfdc_id': lead_model.existing_account__c if lead_model.existing_account__c is not None else lead_model.convertedaccountid, 'role': lead_model.title}
            lead_dict[email] = temp_dict
        return lead_dict

    def init_contact_service(self, mysql_uri):
        logger.info('Initilizating Mysql Connection ..')
        try:
            app = Flask(__name__)
            app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
            contact_db.app = app
            contact_db.init_app(app)
        except Exception as e:
            logger.error('Error Connecting to Mysql {msg}'.format(msg=e.message))
            raise

    @staticmethod
    def get_all_contacts():
        logger.info('get_all_contacts()')
        contact_dict = {}
        try:
            contact_model_list = ContactModel.query.filter((ContactModel.email != None) & (ContactModel.accountid != None)).all()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise
        for contact_model in contact_model_list:
            email = contact_model.email.lower()
            temp_dict = {'sfdc_id': contact_model.accountid,'role': contact_model.title}
            contact_dict[email] = temp_dict
        return contact_dict

    def init_account_service(self, mysql_uri):
        logger.info('Initilizating Mysql Connection ..')
        try:
            app = Flask(__name__)
            app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
            account_db.app = app
            account_db.init_app(app)
        except Exception as e:
            logger.error('Error Connecting to Mysql {msg}'.format(msg=e.message))
            raise

    @staticmethod
    def get_all_accounts():
        logger.info('get_all_accounts()')
        account_list = []

        try:
            account_model_list = AccountModel.query.filter(AccountModel.website != None).all()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise
        for account_model in account_model_list:
            temp_dict = {'website': account_model.website.lower(),'sfdc_id': account_model.pk_id}
            account_list.append(temp_dict)
        return pd.DataFrame(account_list)


    @staticmethod
    def update_data(academy_data):
        try:
            academy_db.session.add(academy_data)
            academy_db.session.commit()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            academy_db.session.rollback()
            raise

    @staticmethod
    def bulk_insert_data(academy_data_list):
        try:
            academy_db.session.bulk_update_mappings(AcademyModel, academy_data_list)
            academy_db.session.commit()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            academy_db.session.rollback()
            raise

    @staticmethod
    def bulk_update_data(academy_data_list):
        try:
            academy_db.session.bulk_update_mappings(AcademyModel, academy_data_list)
            academy_db.session.commit()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            academy_db.session.rollback()
            raise

    @staticmethod
    def get_count():
        logger.info('get_counts()')
        count = None
        try:
            count = AcademyModel.query.count()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise

        return count

    @staticmethod
    def find_max(table_column):
        try:
            return academy_db.session.query(func.max(table_column)).scalar()
        except Exception as e:
            logger.error('Error getting data from MySQL {msg}'.format(msg=e.message))
            raise

    @staticmethod
    def upsert_acamedy_data(academy_model_data_list):
        for academy_data in academy_model_data_list:
            home_sql = 'insert into '+config.MYSQL_CONN['academy_tbl']+'(user_id, course_id, title, email, progress, start_ts, finish_ts, dsa_last_updated_ts) '
            ins_sql = home_sql + 'values({user_id}, {course_id}, "{title}", "{email}", {progress}, "{start_ts}", "{finish_ts}", "{dsa_last_updated_ts}") ' \
                                 'on duplicate key update progress={progress}, finish_ts="{finish_ts}", dsa_last_updated_ts="{dsa_last_updated_ts}"'.format(
                    user_id=academy_data['user_id'], course_id=academy_data['course_id'], title=academy_data['title'], email=academy_data['email'], progress=academy_data['progress'], start_ts=academy_data['start_ts'] if academy_data['start_ts'] is not None else "null",
                    finish_ts=academy_data['finish_ts'] if academy_data['finish_ts'] is not None else "null", dsa_last_updated_ts=academy_data['dsa_last_updated_ts'] if academy_data['dsa_last_updated_ts'] is not None else "null")
            sql = ins_sql.replace('\"null\"', 'null')
            #TODO: Feb-08: Fix the upsert string replace null
            try:
                academy_db.session.execute(sql)
            except Exception as e:
                logger.error('Error on Upsert data to Mysql {msg}'.format(msg=e.message))
                academy_db.session.rollback()

        academy_db.session.commit()