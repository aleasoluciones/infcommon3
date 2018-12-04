#!/bin/bash

find . -name *pyc* -delete
source "dev/env_develop"

echo
echo "Starting docker-compose..."
echo "----------------------------------------------------------------------"
docker-compose -f dev/devdocker/docker-compose.yml up -d
echo "->waiting everything is up and running..."
sleep 4
echo "->lets go"

echo
echo "Running Integration tests"
echo "----------------------------------------------------------------------"
echo
mamba -f progress `find . -maxdepth 2 -type d -name "integration_specs" | grep -v systems`
MAMBA_RETCODE=$?

echo
echo "Stoping docker-compose..."
echo "----------------------------------------------------------------------"
docker-compose -f dev/devdocker/docker-compose.yml stop
docker-compose -f dev/devdocker/docker-compose.yml rm -f

exit $MAMBA_RETCODE
