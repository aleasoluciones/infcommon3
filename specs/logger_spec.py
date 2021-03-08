from infcommon import logger

with description('logger specs'):
    with context('when logging INFO level'):
        with it('shows message'):
            logger.info('Printing logger info message because TEST_MODE is not set')
