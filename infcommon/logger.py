import os
import logging
import signal

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations import DidNotEnable
from infcommon import logging_utils


TEST_MODE_NOT_ENABLED = os.environ.get('TEST_MODE') is None


class Logger:
    def critical(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', True)
        self._log(logging.critical, message, exc_info=exc_info, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', True)
        self._log(logging.error, message, exc_info=exc_info, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log(logging.warning, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(logging.info, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log(logging.debug, message, *args, **kwargs)

    def set_level(self, level):
        logging.getLogger().setLevel(level)

    def _log(self, function_to_call, message, *args, **kwargs):
        if TEST_MODE_NOT_ENABLED:
            function_to_call(message, *args, **kwargs)


infrastructure_logger = Logger()


def set_level(level):
    global infrastructure_logger
    infrastructure_logger.set_level(level)


def configure_sentry_if_exists_env_variable(traces=True):
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if not sentry_dsn:
        logging.info("SENTRY_DSN is not set")
        return

    integrations = []

    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.CRITICAL)
    integrations.append(sentry_logging)

    try:
        from sentry_sdk.integrations.redis import RedisIntegration
        import redis
        integrations.append(RedisIntegration())
    except (ModuleNotFoundError, sentry_sdk.integrations.DidNotEnable):
        pass

    try:
        from sentry_sdk.integrations.tornado import TornadoIntegration
        import tornado
        integrations.append(TornadoIntegration())
    except (ModuleNotFoundError, sentry_sdk.integrations.DidNotEnable):
        pass

    if not traces:
        logging.info("SENTRY traces are not enabled")
        sentry_sdk.init(sentry_dsn,
                        traces_sample_rate=0.0,
                        integrations=integrations)
        return

    logging.info("SENTRY traces are enabled")
    sentry_sdk.init(sentry_dsn,
                    traces_sample_rate=1.0,
                    integrations=integrations)


configure_sentry_if_exists_env_variable(traces=False)


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

signal.signal(signal.SIGRTMIN, lambda signal, frame: configure_sentry_if_exists_env_variable(traces=False))
signal.signal(signal.SIGRTMAX, lambda signal, frame: configure_sentry_if_exists_env_variable(traces=True))
