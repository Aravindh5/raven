__author__ = 'Valtanix Inc.,'

import os
import logging
import logging.handlers
import logging.config
import config

logger = logging.getLogger(config.LOG_ALIAS)

class LogHandler():

    def __init__(self, dir=None, file='raven.log', log_level='DEBUG', parallel_no=None):

        # If already initialized then simply return
        if logger.handlers != []:
            return

        if dir is None:
            dir = config.LOG_DIR

        # file = 'raven_' + str(os.getpid()) + '_' + str(parallel_no) + '.log'
        file = config.PROJECT_NAME + '.log'
        self.log_file = os.path.join(dir, file)
        
        self.log_level = logging.getLevelName(log_level)

        logger.setLevel(self.log_level)
        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=config.LOG_MAX_BYTES, backupCount=config.LOG_BACKUP_COUNT)
        log_format = '%(asctime)s - %(threadName)s - %(module)-18s - %(lineno)3d - %(funcName)-24s - %(levelname)-5s - %(message)s'
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)

        # Show same logs in console as well
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        console_handler.setLevel(self.log_level)
        logger.addHandler(console_handler)

        logger.info('#### Logging initialized ####')

