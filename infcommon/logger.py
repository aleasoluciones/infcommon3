# -*- coding: utf-8 -*-

import os
import logging
import traceback
from infcommon import logging_utils


class Logger(object):

    def critical(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', True)
        logging.critical(self._generate_message_with_traceback(message), exc_info=exc_info, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', True)
        logging.error(self._generate_message_with_traceback(message), exc_info=exc_info, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        logging.warning(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        logging.info(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        logging.debug(message, *args, **kwargs)

    def set_level(self, level):
        logging.getLogger().setLevel(level)

    def _generate_message_with_traceback(self, message):
        return 'message: {message}, traceback: {traceback}'.format(message=message, traceback=traceback.format_stack())


infrastructure_logger = Logger()


def set_level(level):
    global infrastructure_logger
    infrastructure_logger.set_level(level)


TEST_MODE_NOT_ENABLED = os.environ.get('TEST_MODE') is None

def configure_sentry_if_exists_env_variable():
    sentry_dsn_env = os.environ.get('SENTRY_DSN')
    if sentry_dsn_env is not None:
        sentry_conf = {'level': 'CRITICAL',
                        'class': 'raven.handlers.logging.SentryHandler',
                        'dsn': sentry_dsn_env}
        logging_utils.add_handler('sentry', sentry_conf)

configure_sentry_if_exists_env_variable()

def info(message, *args, **kwargs):
    _log('info', message, args, kwargs)

def debug(message, *args, **kwargs):
    _log('debug', message, args, kwargs)

def warning(message, *args, **kwargs):
    _log('warning', message, args, kwargs)

def error(message, *args, **kwargs):
    _log('error', message, args, kwargs)

def critical(message, *args, **kwargs):
    _log('critical', message, args, kwargs)

def _log(level, message, args, kwargs):
   if TEST_MODE_NOT_ENABLED:
        getattr(infrastructure_logger, level)(message, *args, **kwargs)

