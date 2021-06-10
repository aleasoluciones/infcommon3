# infcommon3

[![Build status](https://api.travis-ci.com/aleasoluciones/infcommon.svg?branch=master)](https://travis-ci.com/aleasoluciones/infcommon3)

This library contains some utils that are commonly used in most of the Alea's projects.

## Installation

This library works with **Python 3.7**.

```bash
mkvirtualenv infcommon3 -p $(which python3.7)
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
pip install -r requirements.txt
```

## Logging configuration

* You can set the SENTRY_DNS environment variable to use Sentry as logger handler.
* To disable the logs, set the environment variable TEST_MODE (e.g. when executing the tests we don't want logs to be printed or breaking the execution).
