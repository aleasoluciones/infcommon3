# -*- coding: utf-8 -*-

import os

from infcommon.factory import Factory
from infcommon.yaml_reader.yaml_reader import YamlReader
from infcommon.yaml_reader.yaml_loaders import DirectoryYamlLoader


DEFAULT_PATH_ENVIRONMENT_VARIABLE_NAME = 'CONF_FILE'


def yaml_reader(path=None):
    path = path or os.environ[DEFAULT_PATH_ENVIRONMENT_VARIABLE_NAME]
    return Factory.instance('yaml_reader',
                            lambda: YamlReader(path))


def directory_yaml_loader(path=None):
    return Factory.instance('directory_yaml_loader',
                            lambda: DirectoryYamlLoader(path)
                            )
