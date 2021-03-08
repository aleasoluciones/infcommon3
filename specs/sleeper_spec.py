from doublex import *
from expects import *
from doublex_expects import *

import datetime

from infcommon import clock as clock_module

IRRELEVANT_TIME = datetime.datetime.now()
IRRELEVANT_SECONDS = 2
IRRELEVANT_SLEEP = datetime.timedelta(seconds=IRRELEVANT_SECONDS)

with description('Sleeper specs'):
    with before.each:
        self.clock = Stub()
        self.time_module = Spy()
        self.sleeper = clock_module.Sleeper(self.clock, self.time_module)
        when(self.clock).now().returns(IRRELEVANT_TIME)

    with it('calls time module'):
        self.sleeper.sleep(IRRELEVANT_SECONDS)

        expect(self.time_module.sleep).to(have_been_called_with(IRRELEVANT_SECONDS))


    with it('sleeps till time'):
        self.sleeper.sleep_until(IRRELEVANT_TIME + IRRELEVANT_SLEEP)

        expect(self.time_module.sleep).to(have_been_called_with(IRRELEVANT_SECONDS))

    with context('when is expected time'):
        with it('doesnt sleep'):
            self.sleeper.sleep_until(IRRELEVANT_TIME)

            expect(self.time_module.sleep).not_to(have_been_called)


