# infcommon3 documentation

[![Build status](https://secure.travis-ci.org/aleasoluciones/infcommon.svg?branch=master)](https://secure.travis-ci.org/aleasoluciones/infcommon3)


## Installation

### Requirements

Add python 3.5 or above to your Linux host
```
$ sudo add-apt-repository ppa:fkrull/deadsnakes
$ sudo apt-get update
$ sudo apt-get install python-virtualenv python3.5 python3.5-dev
```

### Configure virtual environment
You can use virtualenv wrapper (mkvirtualenv)
```
$ mkvirtualenv -p /usr/bin/python3.5 infcommon3
```
Or default virtualenv
```
$ cd /home/USER/DEV_WORKSPACE/infcommon3
$ virtualenv -p /usr/bin/python3.5 infcommon3_ve
$ source infcommon3ve/bin/activate
```

Remember that virtualenv creates the virtual_env_directory directly at the actual path

Remember to exclude virtualenv directory from git

### Install all python packages
Enter to your virtualenv project and run `dev/setup_venv.sh`


## Run the tests
Enter to your virtualenv project 
Run `dev/all-tests.sh`

## Logger documentation
* **VERY IMPORTANT**: If you want, you can set SENTRY_DNS environment variable to use Sentry as logger handler.
* For disabling the logs, set the environment variable TEST_MODE (e.g. when executing the tests we don't want logs to be printed or breaking the execution). This is currently done in env_develop.

## Usage of this components in another project
To use this library put below line at your *requirements.txt*

```
-e git+https://github.com/aleasoluciones/infcommon3.git@#egg=infcommon

```

now run pip to install dependencies:
```
pip install -r requirements.txt
```
