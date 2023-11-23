import yaml
import time
import logging
import os
import re

from infcommon.info_container.info_container import InfoContainer



class YamlReaderNotValidFileError(BaseException):
    pass


class YamlReader:
    NO_CACHE = 0

    def __init__(self, path, cache_time_in_sec=NO_CACHE):
        self._path = path
        self._MAX_SECS = cache_time_in_sec
        self._cache = None
        self._cache_time = 0
        self._cache_hits = 0
        self._inverted = None
        self._inverted_time = 0
        self._inverted_hits = 0

    def get(self, key):
        self._update_cache()
        return self._cache.get(key)

    def get_info_container(self):
        self._update_cache()
        return InfoContainer(self._cache, return_none=True)

    def get_key_by(self, value):
        self._update_cache()
        for key, value_ in self._cache.items():
            if not isinstance(value_, bool) and value in value_:
                return key

    def get_all(self):
        self._update_cache()
        return self._cache

    def __getitem__(self, key):
        self._update_cache()
        return self._cache[key]

    def _update_cache(self):
        if self._MAX_SECS == self.NO_CACHE:
            self._cache = self._load_file()
            return
        now = time.monotonic()
        if self._cache is None or self._cache_time + self._MAX_SECS < now:
            logging.warning('%s %s %s %s %s %d, %s, %d' % ('UPDATE CACHE:', 'file:', self._path, 'invalid cache', 'hits:', self._cache_hits, 'delta:', now - self._cache_time))
            self._cache_hits = 0
            self._cache_time = now
            self._cache = self._load_file()
            return
        self._cache_hits += 1

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
                    with open(f'{folder_path}/{match[1]}') as include_f:
                        content.extend(iter(include_f))
                else:
                    content.append(line)
        return yaml.load(''.join(content), Loader=yaml.FullLoader)
