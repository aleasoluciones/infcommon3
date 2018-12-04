#!/bin/bash

echo
echo "Running Unit tests"
echo "----------------------------------------------------------------------"
echo
mamba -f progress specs
UNITTESTS_RETCODE=$?
exit $UNITTESTS_RETCODE
