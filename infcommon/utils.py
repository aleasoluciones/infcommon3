import time
import datetime
import logging

MIN_SLEEP_TIME = 0.5
MAX_RECONNECTION_TIME = 10
SUCESSFUL_RECONNECTION_TIME = 30


def do_stuff_with_exponential_backoff(exceptions, stuff_func, *args, **kwargs):
    try_num = 1
    while True:
        try:
            t1 = datetime.datetime.now()
            return stuff_func(*args, **kwargs)
        except exceptions as exc:
            _log_to_critical_or_error(try_num, exc)
            try_num = _calculate_try_number(t1, try_num)
            _sleep_for_reconnect(try_num, exc)


def _sleep_for_reconnect(try_num, exception):
    reconnect_sleep_time = min(MAX_RECONNECTION_TIME, (try_num**2)*MIN_SLEEP_TIME)
    logging.info("Waiting for reconnect try {} sleeping {}s after {}".format(try_num, reconnect_sleep_time, repr(exception)))
    time.sleep(reconnect_sleep_time)


def _log_to_critical_or_error(try_num, exception):
    if try_num % 5 == 0:
        logging.critical("Error with exponential backoff: " + repr(exception), exc_info=True)
    else:
        logging.error("Error with exponential backoff: " + repr(exception))


def _calculate_try_number(t1, try_num):
    if datetime.datetime.now() - t1 > datetime.timedelta(seconds=SUCESSFUL_RECONNECTION_TIME):
        try_num = 1
    else:
        try_num += 1
    return try_num

