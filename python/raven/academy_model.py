import config
from flask_sqlalchemy import SQLAlchemy

academy_db = SQLAlchemy()

class AcademyModel(academy_db.Model):

    __tablename__ = config.MYSQL_CONN['academy_tbl']
    user_id = academy_db.Column(academy_db.Integer(), primary_key=True)
    course_id = academy_db.Column(academy_db.Integer(), primary_key=True)
    title = academy_db.Column(academy_db.String(255))
    email = academy_db.Column(academy_db.String(254))
    sfdc_id = academy_db.Column(academy_db.String(18))
    role = academy_db.Column(academy_db.String())
    start_ts = academy_db.Column(academy_db.DateTime)
    finish_ts = academy_db.Column(academy_db.DateTime)
    progress = academy_db.Column(academy_db.Integer())
    dsa_last_updated_ts = academy_db.Column(academy_db.DateTime)
    last_updated_ts = academy_db.Column(academy_db.DateTime)
