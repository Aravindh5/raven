from marshmallow import Schema, fields, ValidationError, pre_load, post_load, validates, validates_schema, validate
import datetime
import logging
import config

logger = logging.getLogger(config.LOG_ALIAS)

class AcademyDataSchema(Schema):

    uid = fields.Int(required=True, allow_none=False)
    nid = fields.Int(required=True, allow_none=False)
    title = fields.Str(required=True)
    email = fields.Str(required=True, allow_none=False)
    started = fields.Int()
    finished = fields.Int()
    updated = fields.Int()
    progress = fields.Int(required=False)

    email_extract = fields.Email()
    start_ts_extract = fields.DateTime()
    finish_ts_extract = fields.DateTime()
    dsa_last_updated_ts_extract = fields.DateTime()


    @post_load
    def process_email(self, data):
        email = data['email']
        if email:
            try:
                data['email_extract'] = email
            except Exception as e:
                msg = 'Cannot extract email'
                raise ValidationError('Invalid email FOUND {value} ALLOWED {msg}'.format(value=email, msg=msg))

        return data

    @post_load
    def process_started(self, data):
        started = data['started']
        if started:
            try:
                data['start_ts_extract'] = self.epoch_to_datetime(started)
            except Exception as e:
                msg = 'Cannot extract start Timestamp'
                raise ValidationError('Invalid time FOUND {value} ALLOWED {msg}'.format(value=started, msg=msg))
        else :
            data['start_ts_extract'] = None
        return data

    @post_load
    def process_finished(self, data):
        finished = data['finished']
        if finished:
            try:
                data['finish_ts_extract'] = self.epoch_to_datetime(finished)
            except Exception as e:
                msg = 'Cannot extract finish Timestamp'
                raise ValidationError('Invalid time FOUND {value} ALLOWED {msg}'.format(value=finished, msg=msg))
        else :
            data['finish_ts_extract'] = None
        return data

    @post_load
    def process_updated(self, data):
        updated = data['updated']
        if updated:
            try:
                data['dsa_last_updated_ts_extract'] = self.epoch_to_datetime(updated)
            except Exception as e:
                msg = 'Cannot extract updated Timestamp'
                raise ValidationError('Invalid time FOUND {value} ALLOWED {msg}'.format(value=updated, msg=msg))
        else :
            data['dsa_last_updated_ts_extract'] = None
        return data



    def epoch_to_datetime(self, epoch_time):
        return datetime.datetime.fromtimestamp(float(epoch_time))


class AcademyData(object):

    # TODO Feb-05, Add SFDC_ID
    def __init__(self, user_id=None, course_id=None, title=None, email=None, start_ts=None, finish_ts=None, dsa_last_updated_ts=None,
                 progress=None):
        self.user_id = user_id
        self.course_id = course_id
        self.title = title
        self.email = email
        self.start_ts = start_ts
        self.finish_ts = finish_ts
        self.dsa_last_updated_ts = dsa_last_updated_ts
        self.progress = progress

    @staticmethod
    def _create_academy_model_data(data):

        # logger.info('_create_academy_model_data()')
        academy_data = AcademyData(
            user_id=data['uid'],
            course_id=data['nid'],
            title=data['title'],
            email=data['email_extract'],
            start_ts=data['start_ts_extract'],
            finish_ts=data['finish_ts_extract'],
            dsa_last_updated_ts=data['dsa_last_updated_ts_extract'],
            progress=data['progress']
        )

        data, errors = AcademyModelSchema().dump(academy_data)

        return data, errors


class AcademyModelSchema(Schema):
    user_id = fields.Int(required=True, allow_none=False)
    course_id = fields.Int(required=True, allow_none=False)
    title = fields.Str(required=True)
    email = fields.Str(required=True, allow_none=False)
    start_ts = fields.DateTime('%Y-%m-%d %H:%M:%S')
    finish_ts = fields.DateTime('%Y-%m-%d %H:%M:%S')
    dsa_last_updated_ts = fields.DateTime('%Y-%m-%d %H:%M:%S')
    progress = fields.Int(required=False)