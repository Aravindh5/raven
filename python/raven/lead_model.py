import config
from flask_sqlalchemy import SQLAlchemy

lead_db = SQLAlchemy()

class LeadModel(lead_db.Model):
    __tablename__ = config.MYSQL_CONN['lead_tbl']
    email = lead_db.Column(lead_db.String(80), primary_key=True)
    existing_account__c = lead_db.Column(lead_db.String(18))
    convertedaccountid = lead_db.Column(lead_db.String(18))
    title = lead_db.Column(lead_db.String())