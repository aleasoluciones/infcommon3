# infcommon3

[![CI](https://github.com/aleasoluciones/infcommon3/actions/workflows/ci.yml/badge.svg)](https://github.com/aleasoluciones/infcommon3/actions/workflows/ci.yml)
![Python versions supported](https://img.shields.io/badge/supports%20python-3.9%20|%203.10%20|%203.11-blue.svg)


This library contains some utils that are commonly used in most of the Alea's projects.

## Installation

```bash
mkvirtualenv infcommon3 -p $(which python3)
workon infcommon3
source dev/env_develop
dev/setup_venv.sh
```

## Running the tests

```bash
all_tests
```

## Usage of this library in another project

To use this library add the line below to your *requirements.txt*:

```
-e git+https://github.com/aleasoluciones/infcommon3.git@#egg=infcommon

```

Then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Logging configuration

* You can set the SENTRY_DNS environment variable to use Sentry as logger handler.
* To disable the logs, set the environment variable TEST_MODE (e.g. when executing the tests we don't want logs to be printed or breaking the execution).
