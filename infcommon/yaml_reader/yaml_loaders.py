import os
import re
import glob
import yaml

from infcommon.yaml_reader.exceptions import DuplicatedKeyError
from infcommon import logger


class DirectoryYamlLoader:
    def __init__(self, path):
        self._path = path

    def load_all(self):
        result = {}
        for filename in self._sync_files():
            file_data = self._load_data_from_file(filename)
            if self._keys_are_already_used(result, file_data):
                exception_message = f'file:{filename} keys:{file_data.keys()}'
                raise DuplicatedKeyError(exception_message)
            if file_data:
                result |= file_data
        return result

    def _sync_files(self):
        filenames = list(glob.glob(f'{self._path}/*.y*ml'))
        return [f'{self._path}/{os.path.basename(filename)}' for filename in filenames]

    def _load_data_from_file(self, filename):
        try:
            content = []
            with open(filename) as f:
                for line in f:
                    if match := re.match('^!include (.*$)', line):
                        folder_path = os.path.dirname(filename)
                        with open(f'{folder_path}/{match[1]}') as include_f:
                            content.extend(iter(include_f))
                    else:
                        content.append(line)
            return yaml.load(''.join(content), Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            logger.error(f"Error loading file: {filename} {exc}")
            return {}

    def _keys_are_already_used(self, all_dict, current_dict):
        if all_dict != {} and current_dict != None:
            return len(set(all_dict.keys()) & set(current_dict.keys())) > 0
