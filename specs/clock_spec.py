# -*- coding: utf-8 -*-

from doublex import *
from expects import *
from doublex_expects import *

import datetime

from infcommon import clock as clock_module

with description('Clock specs') as self:
    with it('calls collaborator for today'):
        date_obj = Spy()
        clock = clock_module.Clock(date_obj=date_obj)
        clock.today()
        expect(date_obj.today).to(have_been_called)

    with it('calls collaborator for now'):
        datetime_obj = Spy()
        clock = clock_module.Clock(datetime_obj=datetime_obj)
        clock.now()
        expect(datetime_obj.now).to(have_been_called)

    with it('calls collaborator for utcnow'):
        datetime_obj = Spy()
        clock = clock_module.Clock(datetime_obj=datetime_obj)
        clock.utcnow()
        expect(datetime_obj.utcnow).to(have_been_called)

    with context('working with timestamps'):
        with it('checks aproximated time stamps'):
            now = clock_module.Clock().now()
            utc_timestamp = clock_module.Clock().utctimestampnow()
            local_from_timestamp = clock_module.Clock.fromtimestamp(utc_timestamp)
            expect(clock_module.Clock.aprox(now, local_from_timestamp)).to(be_true)

        with context('using conversion'):
            with it('checks aproximated timestamps '):
                # This conversion loose some microseconds so we only check if the
                # conversion is approximately correct
                now = datetime.datetime.now()
                ts = clock_module.Clock.timestamp(now)
                now_from_ts = clock_module.Clock.fromtimestamp(ts)
                expect(clock_module.Clock.aprox(now, now_from_ts)).to(be_true)

    with context('working with time ranges'):
        with before.each:
            self.start_time = datetime.time(hour=1)
            self.end_time = datetime.time(hour=2)
            self.datetime_obj = Stub()

        with context('when current time is in range'):
            with it('returns true'):
                now = datetime.datetime(year=1981, month=1, day=1, hour=1, minute=30)
                when(self.datetime_obj).now().returns(now)
                clock = clock_module.Clock(datetime_obj=self.datetime_obj)

                now_in_range = clock.is_current_time_in_range(start=self.start_time, end=self.end_time)

                expect(now_in_range).to(be_true)

        with context('when current time is NOT in range'):
            with it('returns false'):
                now = datetime.datetime(year=1981, month=1, day=1, hour=3)
                when(self.datetime_obj).now().returns(now)
                clock = clock_module.Clock(datetime_obj=self.datetime_obj)

                now_in_range = clock.is_current_time_in_range(start=self.start_time, end=self.end_time)

                expect(now_in_range).to(be_false)

        with context('when current time matches start time'):
            with it('returns true'):
                now = datetime.datetime(year=1981, month=1, day=1, hour=1)
                when(self.datetime_obj).now().returns(now)
                clock = clock_module.Clock(datetime_obj=self.datetime_obj)

                now_in_range = clock.is_current_time_in_range(start=self.start_time, end=self.end_time)

                expect(now_in_range).to(be_true)

        with context('when current time matches end time'):
            with it('returns false'):
                now = datetime.datetime(year=1981, month=1, day=2, hour=2)
                when(self.datetime_obj).now().returns(now)
                clock = clock_module.Clock(datetime_obj=self.datetime_obj)

                now_in_range = clock.is_current_time_in_range(start=self.start_time, end=self.end_time)

                expect(now_in_range).to(be_false)

    with context('calculating timestamp from xxx days ago for a given timestamp'):
        with it('returns the timestamp from xxx days ago'):
            now = clock_module.Clock().now()
            timestamp = clock_module.Clock().timestamp(now)
            days_ago = 30

            result = clock_module.Clock.timestamp_from_days_ago(timestamp, days=days_ago)

            expected_timestamp = clock_module.Clock.timestamp(now - datetime.timedelta(days=days_ago))
            expect(result).to(equal(expected_timestamp))
