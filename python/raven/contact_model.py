import config
from flask_sqlalchemy import SQLAlchemy

contact_db = SQLAlchemy()

class ContactModel(contact_db.Model):
    __tablename__ = config.MYSQL_CONN['contact_tbl']
    email = contact_db.Column(contact_db.String(80), primary_key=True)
    accountid = contact_db.Column(contact_db.String(18))
    title = contact_db.Column(contact_db.String())