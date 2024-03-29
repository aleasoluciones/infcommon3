import os

from infcommon.factory import Factory
from infcommon.settings_retriever.settings_retriever import SettingsRetriever
from infcommon.yaml_reader.yaml_reader import YamlReader


def _settings_file(file_name=None):
    if not file_name:
        return {}
    return YamlReader(file_name)


def settings_retriever(file_name=None):
    all_environment_values = dict(os.environ)
    settings_file = _settings_file(file_name)
    settings_retriever_id = 'settings_retriever_{}'.format(file_name if file_name else "default")
    return Factory.instance(settings_retriever_id,
                            lambda: SettingsRetriever(all_environment_values, settings_file))
