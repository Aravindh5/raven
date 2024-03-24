__author__ = 'Valtanix Inc.,'

import os
import yaml
from collections import OrderedDict


MODEL_NAME = 'Raven - Machine Learning'
PROJECT_NAME = 'raven'
# yaml.load by default gives unordered dictionary. This code preserves the order
# That way it is easy to maintain the yaml file.
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

# Constants
LOG_ALIAS = 'raven_log'
CONFIG_FILE = 'raven.yml'

# Configuration file
base_dir_name = os.path.dirname(os.path.abspath(__file__))
dir_name = base_dir_name + os.sep + '..' + os.sep + 'config'
config_path = os.path.join(dir_name, CONFIG_FILE)
data = ordered_load(file(config_path), yaml.SafeLoader)
#  print(yaml.dump(data))

# Logging
LOG_DIR = data.get('log_dir', base_dir_name + os.sep + '..' + os.sep + 'logs')
LOG_MAX_BYTES = data.get('log_max_bytes', 10485760)
LOG_BACKUP_COUNT = data.get('log_backup_count', 5)

REST_END_POINT = data.get('rest_end_point', None)
assert(REST_END_POINT is not None)

MYSQL_CONN = data.get('mysql_conn', None)
assert(MYSQL_CONN is not None)

MYSQL_COMMIT_EVERY = data.get('mysql_commit_every', 100)
FREE_EMAIL_PROVIDERS = data.get('free_email_provider_file', '../data/free_email_providers.csv')
DATA_DIR = data.get('data_dir', '../data')