import os
import glob
import yaml

from infcommon.yaml_reader.exceptions import DuplicatedKeyError


class DirectoryYamlLoader:
    def __init__(self, path):
        self._path = path

    def load_all(self):
        result = {}
        for filename in self._sync_files():
            file_data = self._load_data_from_file(filename)
            if self._keys_are_already_used(result, file_data):
                exception_message = 'file:{} keys:{}'.format(filename, file_data.keys())
                raise DuplicatedKeyError(exception_message)
            result.update(file_data)
        return result

    def _sync_files(self):
        filenames = [filename for filename in glob.glob(self._path + '/*[.ya?ml]')]
        filenames_with_absolute_path = ['{}/{}'.format(self._path, os.path.basename(filename)) for filename in filenames]
        return filenames_with_absolute_path

    def _load_data_from_file(self, filename):
        with open(filename, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                return {}

    def _keys_are_already_used(self, all_dict, current_dict):
        return len(set(all_dict.keys()) & set(current_dict.keys())) > 0
