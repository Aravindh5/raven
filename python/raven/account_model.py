import config
from flask_sqlalchemy import SQLAlchemy

account_db = SQLAlchemy()

class AccountModel(account_db.Model):
    __tablename__ = config.MYSQL_CONN['account_tbl']
    pk_id = account_db.Column(account_db.String(18), primary_key=True)
    website = account_db.Column(account_db.String)
