# coding=utf-8
# File for common shared config for developers

# Logging config that uses files
import os
import sys

#Environment Variables
BASE_TEST_URL = 'http://localhost:8000' if 'BASE_TEST_URL' not in os.environ else os.environ['BASE_TEST_URL']
DEFAULT_GDRIVE_EMAIL = 'GDRIVE EMAIL ENVIRONMENT VARIABLE NOT SET' if 'DEFAULT_GDRIVE_EMAIL' not in os.environ else os.environ['DEFAULT_GDRIVE_EMAIL']
DEFAULT_GDRIVE_PW = 'GDRIVE PASSWORD ENVIRONMENT VARIABLE NOT SET' if 'DEFAULT_GDRIVE_PW' not in os.environ else os.environ['DEFAULT_GDRIVE_PW']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (u'%(asctime)s [%(process)d] [%(levelname)s] ' +
                       '%(module)s.%(funcName)s::%(lineno)s '
                       '%(message)s'),
        },
        'simple': {
            'format': u'%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'test.log',
            'maxBytes': '1024', # 1 megabyte
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        }
    }
}