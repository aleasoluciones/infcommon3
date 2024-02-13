class SettingsRetrieverKeyNotFoundError(Exception):
    pass


class SettingsRetriever:
    TRUTHY_VALUES = [True, 1, 'True', '1', 'Y']

    def __init__(self, envs, settings_file):
        self._envs = envs
        self._settings_file = settings_file

    def get_value(self, key, default_value=None, fail_on_key_not_found=False):
        if key in self._envs:
            return self._envs.get(key)
        file_value = self._settings_file.get(key)
        if file_value is not None:
            return file_value
        if fail_on_key_not_found:
            raise SettingsRetrieverKeyNotFoundError()
        return default_value

    def get_int(self, key, default_value=None):
        result_value = self.get_value(key, default_value)
        return int(result_value)

    def get_bool(self, key, default_value=None):
        result_value = self.get_value(key, default_value)
        if result_value in self.TRUTHY_VALUES:
            return True
        return False
