#!/bin/bash

dev/unit_tests.sh
UNIT_TEST_RETURN_CODE=$?
dev/integration_tests.sh
INTEGRATION_TEST_RETURN_CODE=$?

RETCODE=$(($UNIT_TEST_RETURN_CODE||$INTEGRATION_TEST_RETURN_CODE))
sleep 1
exit $RETCODE
