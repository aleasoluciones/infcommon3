import yaml
import time
import logging

from infcommon.info_container.info_container import InfoContainer


class YamlReaderNotValidFileError(BaseException):
    pass


class YamlReader:

    def __init__(self, path):
        self._path = path
        self._MAX_SECS = 73
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
        self._update_inverted()
        return self._inverted.get(value)

    def get_all(self):
        self._update_cache()
        return self._cache

    def __getitem__(self, key):
        self._update_cache()
        return self._cache[key]

    def _update_cache(self):
        now = time.monotonic()
        if self._cache is None or self._cache_time + self._MAX_SECS < now:
            logging.warning('%s %s %s %s %s %d, %s, %d' % ('RAMONA:', 'file:', self._path, 'invalid cache', 'hits:', self._cache_hits, 'delta:', now - self._cache_time))
            self._cache_hits = 0
            self._cache_time = now
            self._cache = self._load_file()
            return
        self._cache_hits += 1

    def _update_inverted(self):
        self._update_cache()
        now = time.monotonic()
        if self._inverted is None or self._inverted_time + self._MAX_SECS < now:
            logging.warning('%s %s %s %s %s %d, %s, %d' % ('RAMONA:', 'file:', self._path, 'invalid inverted cache', 'hits:', self._inverted_hits, 'delta:', now - self._inverted_time))
            self._inverted_hits = 0
            self._inverted_time = now
            self._inverted = dict()
            for key, value in self._cache.items():
                if not isinstance(value, bool):
                    # We should handle repeated values, well the original code returns the first match ...
                    # Only store the first match
                    if value in self._inverted:
                        continue
                    self._inverted[value] = key
            return
        self._inverted_hits += 1

    def _load_file(self):
        with open(self._path) as f:
            try:
                content = yaml.load(f, Loader=yaml.FullLoader)
                return content
            except yaml.error.MarkedYAMLError as exc:
                raise YamlReaderNotValidFileError(str(exc))
