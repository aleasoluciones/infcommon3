# -*- coding: utf-8 -*-

import yaml

from infcommon.info_container.info_container import InfoContainer


class YamlReaderNotValidFileError(BaseException):
    pass


class YamlReader(object):

    def __init__(self, path):
        self._path = path

    def get(self, key):
        return self._load_file().get(key)

    def get_info_container(self):
        return InfoContainer(self._load_file(), return_none=True)

    def get_key_by(self, value):
        for key, value_ in self._load_file().iteritems():
            if not isinstance(value_, bool) and value in value_:
                return key

    def get_all(self):
        return self._load_file()

    def __getitem__(self, key):
        return self._load_file()[key]

    def _load_file(self):
        with open(self._path) as f:
            try:
                content = yaml.load(f)
                return content
            except yaml.error.MarkedYAMLError as exc:
                raise YamlReaderNotValidFileError(str(exc))
