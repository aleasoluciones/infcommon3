import os
import re
import yaml

from infcommon.info_container.info_container import InfoContainer


class YamlReaderNotValidFileError(BaseException):
    pass


class YamlReader:

    def __init__(self, path):
        self._path = path

    def get(self, key):
        return self._load_file().get(key)

    def get_info_container(self):
        return InfoContainer(self._load_file(), return_none=True)

    def get_key_by(self, value):
        for key, value_ in self._load_file().items():
            if not isinstance(value_, bool) and value in value_:
                return key

    def get_all(self):
        return self._load_file()

    def __getitem__(self, key):
        return self._load_file()[key]

    def _load_file(self):
        try:
            return self._custom_load_file()
        except yaml.error.MarkedYAMLError as exc:
            raise YamlReaderNotValidFileError(str(exc)) from exc

    def _custom_load_file(self):
        content = []
        with open(self._path) as f:
            for line in f:
                if match := re.match('^!include (.*$)', line):
                    folder_path = os.path.dirname(self._path)
                    with open(f'{folder_path}/{match[1]}', 'r') as include_f:
                        content.extend(iter(include_f))
                else:
                    content.append(line)
        return yaml.load(''.join(content), Loader=yaml.FullLoader)
