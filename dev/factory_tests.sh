#!/bin/bash

SCRIPT_DIR=`dirname $0`
DEVELOP_ENV=$SCRIPT_DIR/env_develop
echo
. $DEVELOP_ENV

for pyc_file in $(find . -path *docker_data* -prune -o -name '*.pyc' -print); do
    rm $pyc_file
done
echo
echo "----------------------------------------------------------------------"
echo "Running Factory tests"
echo "----------------------------------------------------------------------"
echo

python dev/run_factory_tests.py
