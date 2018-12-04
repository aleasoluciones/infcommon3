class SettingsRetriever(object):
    def __init__(self, envs, settings_file):
        self._envs = envs
        self._settings_file = settings_file

    def get_value(self, key, default_value=None):
        envs_value = self._envs.get(key)
        if envs_value:
            return envs_value
        file_value = self._settings_file.get(key)
        if file_value:
            return file_value
        return default_value


