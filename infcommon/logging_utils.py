# -*- coding: utf-8 -*-

import logging
import logging.config
import signal

BASE_CONF= {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
            },
        },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
            },
        },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


def add_handler(handler_name, handler_conf):
    BASE_CONF['handlers'][handler_name] = handler_conf
    BASE_CONF['loggers']['']['handlers'].append(handler_name)
    logging.config.dictConfig(BASE_CONF)

def activate_debug():
    BASE_CONF['handlers']['console']['level'] = 'DEBUG'
    logging.config.dictConfig(BASE_CONF)
    logging.info("Activating debug")

def deactivate_debug():
    BASE_CONF['handlers']['console']['level'] = 'INFO'
    logging.config.dictConfig(BASE_CONF)
    logging.info("Deactivating debug")

signal.signal(signal.SIGUSR1, lambda signal, frame: activate_debug())
signal.signal(signal.SIGUSR2, lambda signal, frame: deactivate_debug())

BASE_CONF['handlers']['console']['level'] = 'INFO'
logging.config.dictConfig(BASE_CONF)
