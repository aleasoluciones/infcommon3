from mamba import describe, context, it, before
from expects import expect, equal, raise_error
from doublex import Stub, when

from infcommon.yaml_reader.yaml_reader import YamlReader
from infcommon.settings_retriever.settings_retriever import SettingsRetriever

A_KEY = 'a_key'
AN_ENVIRONMENT_VALUE = 'an_environment_value'
A_FILE_VALUE = 'a_file_value'
A_DEFAULT_VALUE = 'a_default_value'
A_NUMBER_AS_INTEGER = 23
A_NUMBER_AS_STRING = '23'
A_NON_PARSEABLE_STRING = '5ty'
A_TRUTHY_VALUE_TRUE = 'True'
A_TRUTHY_VALUE_TRUE_BOOL = True
A_TRUTHY_VALUE_ONE = '1'
A_TRUTHY_VALUE_ONE_NUMERIC = 1
A_TRUTHY_VALUE_Y = 'Y'
A_FALSY_VALUE_FALSE = 'False'
A_FALSY_VALUE_ZERO = '0'
A_FALSY_VALUE_N = 'N'
ANYTHING_ELSE = 'f5kN'

with describe('Settings') as self:
    with before.each:
        self.settings_file = Stub(YamlReader)

    with context('FEATURE: get string value'):
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

            with context('variable file is NOT present'):
                with it('returns the default value'):
                    envs = {}
                    settings = SettingsRetriever(envs, self.settings_file)

                    value = settings.get_value(key=A_KEY, default_value=A_DEFAULT_VALUE)

                    expect(value).to(equal(A_DEFAULT_VALUE))

    with context('FEATURE: get parsed integer value'):
        with context('when an environment variable can be parsed to int'):
            with it('returns an integer'):
                envs = {A_KEY: A_NUMBER_AS_STRING}
                settings = SettingsRetriever(envs, self.settings_file)

                value = settings.get_int(key=A_KEY)

                expect(value).to(equal(A_NUMBER_AS_INTEGER))

        with context('when an environment variable cannot be parsed to int'):
            with it('raises an exception'):
                envs = {A_KEY: A_NON_PARSEABLE_STRING}
                settings = SettingsRetriever(envs, self.settings_file)

                def _get_int():
                    return settings.get_int(key=A_KEY)

                expect(_get_int).to(raise_error(ValueError))


    with context('FEATURE: get parsed boolean value'):
        with context('when an environment variable can be parsed to boolean'):
            with context('when truthy values'):
                with context('when a variable is True as a String'):
                    with it('returns True'):
                        envs = {A_KEY: A_TRUTHY_VALUE_TRUE}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(True))

                with context('when a variable is 1 as a String'):
                    with it('returns True'):
                        envs = {A_KEY: A_TRUTHY_VALUE_ONE}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(True))

                with context('when a variable is Y'):
                    with it('returns True'):
                        envs = {A_KEY: A_TRUTHY_VALUE_Y}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(True))

                with context('when a variable is True as a Boolean'):
                    with it('returns True'):
                        envs = {A_KEY: A_TRUTHY_VALUE_ONE_NUMERIC}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(True))

                with context('when a variable is 1 as a Number'):
                    with it('returns True'):
                        envs = {A_KEY: A_TRUTHY_VALUE_TRUE_BOOL}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(True))


            with context('when falsy values'):
                with context('when a variable is False'):
                    with it('returns False'):
                        envs = {A_KEY: A_FALSY_VALUE_FALSE}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(False))

                with context('when a variable is 0'):
                    with it('returns False'):
                        envs = {A_KEY: A_FALSY_VALUE_ZERO}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(False))

                with context('when a variable is N'):
                    with it('returns False'):
                        envs = {A_KEY: A_FALSY_VALUE_N}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(False))

                with context('when a variable is anything else'):
                    with it('returns False'):
                        envs = {A_KEY: ANYTHING_ELSE}
                        settings = SettingsRetriever(envs, self.settings_file)

                        value = settings.get_bool(key=A_KEY)

                        expect(value).to(equal(False))
