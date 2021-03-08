import datetime
import time


class Clock:

    def __init__(self, datetime_obj=datetime.datetime, date_obj=datetime.date):
        self.datetime_obj = datetime_obj
        self.date_obj = date_obj

    def today(self):
        return self.date_obj.today()

    def now(self):
        return self.datetime_obj.now()

    def utcnow(self):
        return self.datetime_obj.utcnow()

    def utctimestampnow(self):
        return self.timestamp(self.now())

    def is_current_time_in_range(self, start, end):
        now = self.now().time()
        return now >= start and now < end

    def timestamp_from_days_ago(self, days):
        return Clock.timestamp(self.now() - datetime.timedelta(days=days))

    @staticmethod
    def timestamp(t):
        # time.mktime requires LOCAL time and returns UTC
        return time.mktime(t.timetuple()) + (t.microsecond / 1000000.0)

    @staticmethod
    def fromtimestamp(ts):
        return datetime.datetime.fromtimestamp(ts)

    @staticmethod
    def aprox(dt1, dt2):
        delta = dt2 - dt1
        return delta.days == 0 and delta.seconds == 0


class Sleeper:

    def __init__(self, clock=Clock(), time_module=time):
        self.clock = clock
        self.time_module = time_module

    def sleep_until(self, time):
        now = self.clock.now()
        time_to_sleep = time - now
        if time_to_sleep > datetime.timedelta(seconds=0):
            self.time_module.sleep(time_to_sleep.seconds)

    def sleep(self, seconds):
        self.time_module.sleep(seconds)
