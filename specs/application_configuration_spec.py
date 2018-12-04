from expects import expect, equal
from doublex import Stub, when

from infcommon.yaml_reader.yaml_reader import YamlReader
from infcommon.settings_retriever.settings_retriever import SettingsRetriever

A_KEY = 'a_key'
AN_ENVIRONMENT_VALUE = 'an_environment_value'
A_FILE_VALUE = 'a_file_value'
A_DEFAULT_VALUE = 'a_default_value'

with describe('Settings'):
    with before.each:
        self.settings_file = Stub(YamlReader)

    with context('when enviroment variable is present'):
        with it('returns enviroment value'):
            envs = {A_KEY: AN_ENVIRONMENT_VALUE}
            settings = SettingsRetriever(envs, self.settings_file)

            value = settings.get_value(key=A_KEY)

            expect(value).to(equal(AN_ENVIRONMENT_VALUE))

    with context('when enviroment variable is NOT present'):
      with context('variable file is present'):
        with it('returns file value'):
            envs = {}
            when(self.settings_file).get(A_KEY).returns(A_FILE_VALUE)
            settings = SettingsRetriever(envs, self.settings_file)

            value = settings.get_value(key=A_KEY)

            expect(value).to(equal(A_FILE_VALUE))

      with context('variable file is NOT Present'):
        with it('returns the default value'):
            envs = {}
            settings = SettingsRetriever(envs, self.settings_file)

            value = settings.get_value(key=A_KEY, default_value=A_DEFAULT_VALUE)

            expect(value).to(equal(A_DEFAULT_VALUE))
