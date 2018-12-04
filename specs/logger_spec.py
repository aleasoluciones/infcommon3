# -*- coding: utf-8 -*-

from infcommon import logger

with description('logger specs'):
    with context('When logging INFO level'):
        with it('xxx'):
            logger.info('PATATA')
