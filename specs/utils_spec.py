from expects import expect, equal
from mamba import description, context, it, before, after

import time
import logging

from infcommon import utils


def create_failing_func(fail_times=0, exception_type=ValueError, success_value='success'):
    call_count = [0]
    def func(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] <= fail_times:
            raise exception_type('fail')
        return success_value
    return func, call_count


with description('do_stuff_with_exponential_backoff') as self:
    with before.each:
        self.original_time_sleep = time.sleep
        self.original_logging_error = logging.error
        self.original_logging_critical = logging.critical
        self.original_logging_info = logging.info

        self.sleep_calls = []
        self.error_calls = []
        self.critical_calls = []
        self.info_calls = []

        def mock_sleep(seconds):
            self.sleep_calls.append(seconds)

        def mock_error(*args, **kwargs):
            self.error_calls.append((args, kwargs))

        def mock_critical(*args, **kwargs):
            self.critical_calls.append((args, kwargs))

        def mock_info(*args, **kwargs):
            self.info_calls.append((args, kwargs))

        time.sleep = mock_sleep
        logging.error = mock_error
        logging.critical = mock_critical
        logging.info = mock_info

    with after.each:
        time.sleep = self.original_time_sleep
        logging.error = self.original_logging_error
        logging.critical = self.original_logging_critical
        logging.info = self.original_logging_info

    with context('when function succeeds on first try'):
        with it('returns the result without retrying'):
            stuff_func, call_count = create_failing_func(fail_times=0)

            result = utils.do_stuff_with_exponential_backoff(Exception, stuff_func)

            expect(result).to(equal('success'))
            expect(call_count[0]).to(equal(1))

        with it('does not sleep'):
            stuff_func, _ = create_failing_func(fail_times=0)

            utils.do_stuff_with_exponential_backoff(Exception, stuff_func)

            expect(self.sleep_calls).to(equal([]))

    with context('when function fails and then succeeds'):
        with it('retries and eventually returns success'):
            stuff_func, call_count = create_failing_func(fail_times=1)

            result = utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(result).to(equal('success'))
            expect(call_count[0]).to(equal(2))

        with it('uses exponential backoff on first retry'):
            stuff_func, _ = create_failing_func(fail_times=1)

            utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(self.sleep_calls).to(equal([2.0]))

        with it('logs error on first failure'):
            stuff_func, _ = create_failing_func(fail_times=1)

            utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(len(self.error_calls)).to(equal(1))

    with context('when function fails multiple times'):
        with it('uses exponential backoff with increasing sleep times'):
            stuff_func, _ = create_failing_func(fail_times=2)

            utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(2.0 in self.sleep_calls).to(equal(True))
            expect(4.5 in self.sleep_calls).to(equal(True))

        with it('caps sleep time at MAX_RECONNECTION_TIME'):
            stuff_func, _ = create_failing_func(fail_times=11)

            utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(10 in self.sleep_calls).to(equal(True))

        with it('logs to critical on 5th failure'):
            stuff_func, _ = create_failing_func(fail_times=5)

            utils.do_stuff_with_exponential_backoff(ValueError, stuff_func)

            expect(len(self.critical_calls)).to(equal(1))

    with context('when function is called with args and kwargs'):
        with it('passes them to the function'):
            received_args = []
            received_kwargs = {}
            def capturing_func(*args, **kwargs):
                received_args.extend(args)
                received_kwargs.update(kwargs)
                return 'result'

            result = utils.do_stuff_with_exponential_backoff(
                Exception, capturing_func, 'arg1', 'arg2', key='value'
            )

            expect(result).to(equal('result'))
            expect(received_args).to(equal(['arg1', 'arg2']))
            expect(received_kwargs).to(equal({'key': 'value'}))

    with context('when handling multiple exception types'):
        with it('catches any exception in the tuple'):
            stuff_func, _ = create_failing_func(fail_times=1)

            result = utils.do_stuff_with_exponential_backoff((ValueError, TypeError), stuff_func)

            expect(result).to(equal('success'))
