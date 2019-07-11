# -*- coding: utf-8 -*-

import os

from infcommon.factory import Factory
from infcommon.yaml_reader.yaml_reader import YamlReader
from infcommon.yaml_reader.yaml_loaders import DirectoryYamlLoader


DEFAULT_PATH_ENVIRONMENT_VARIABLE_NAME = 'CONF_FILE'


def yaml_reader(path=None):
    path = path or os.environ[DEFAULT_PATH_ENVIRONMENT_VARIABLE_NAME]
    yaml_reader_id = 'yaml_reader_{}'.format(path)
    return Factory.instance(yaml_reader_id,
                            lambda: YamlReader(path))


def directory_yaml_loader(path=None):
    directory_yaml_loader_id = 'directory_yaml_loader_{}'.format(path)
    return Factory.instance(directory_yaml_loader_id,
                            lambda: DirectoryYamlLoader(path)
                            )
