import logging
import logging.config
import signal
import contextvars

trace_id_var = contextvars.ContextVar("trace_id", default=None)

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True
    
class TraceIdFormatter(logging.Formatter):
    def format(self, record):
        trace_id = getattr(record, "trace_id", None)
        record.trace_id_str = f"[{trace_id}]" if trace_id else ""
        return super().format(record)

BASE_CONF = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            '()': TraceIdFormatter,
            'format': '[%(asctime)s][%(levelname)s]%(trace_id_str)s %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },

    'filters': {
        'trace_id': {
            '()': TraceIdFilter, 
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'filters': ['trace_id'], 
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


def activate_debug(log_info=True):
    BASE_CONF['handlers']['console']['level'] = 'DEBUG'
    BASE_CONF['disable_existing_loggers'] = True
    logging.config.dictConfig(BASE_CONF)
    if log_info:
        logging.info("Activating debug")


def deactivate_debug(log_info=True):
    BASE_CONF['handlers']['console']['level'] = 'INFO'
    BASE_CONF['disable_existing_loggers'] = False
    logging.config.dictConfig(BASE_CONF)
    if log_info:
        logging.info("Deactivating debug")


signal.signal(signal.SIGUSR1, lambda sig, frame: activate_debug())
signal.signal(signal.SIGUSR2, lambda sig, frame: deactivate_debug())

BASE_CONF['handlers']['console']['level'] = 'INFO'
logging.config.dictConfig(BASE_CONF)
