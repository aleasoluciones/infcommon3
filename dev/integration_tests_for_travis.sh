#!/bin/bash

echo
echo "----------------------------------------------------------------------"
echo "Running Integration tests"
echo "----------------------------------------------------------------------"
echo
mamba -f progress `find . -maxdepth 2 -type d -name "integration_specs" | grep -v systems`
MAMBA_RETCODE=$?
exit $MAMBA_RETCODE
