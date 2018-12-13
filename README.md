# infcommon3 documentation

[![Build status](https://secure.travis-ci.org/aleasoluciones/infcommon.svg?branch=master)](https://secure.travis-ci.org/aleasoluciones/infcommon3)

## How to set up your local development environment

1. Run `source dev/env_develop`
2. Run `dev/setup_venv.sh`

## How to run the tests
Run `dev/all-tests.sh`

## Logger documentation
* **VERY IMPORTANT**: If you want, you can set SENTRY_DNS environment variable to use Sentry as logger handler.
* For disabling the logs, set the environment variable TEST_MODE (e.g. when executing the tests we don't want logs to be printed or breaking the execution). This is currently done in env_develop.

## Usage
To use this library put below line at your *requirements.txt*

```
-e git+https://github.com/aleasoluciones/infcommon3.git@#egg=infcommon

```

now run pip to install dependencies:
```
pip install -r requirements.txt
```
