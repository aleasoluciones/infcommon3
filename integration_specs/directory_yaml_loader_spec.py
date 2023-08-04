import os

from mamba import description, context, it
from expects import expect, equal, raise_error, have_length, contain

from infcommon.yaml_reader.yaml_loaders import DirectoryYamlLoader
from infcommon.yaml_reader.exceptions import DuplicatedKeyError


BASE_PATH = os.path.abspath(f'{os.path.dirname(__file__)}/tests_resources')
A_PATH_WITH_THREE_YAML = 'isp_templates'
NUMBER_OF_TEMPLATES_IN_A_PATH_WITH_TWO_YAML = 4
NUMBER_OF_TEMPLATES_IN_A_PATH_WITH_THREE_YAML = 4
A_PATH_WITH_A_BAD_AND_GOOD_YAML = 'bad_and_good_isp_templates'
NUMBER_OF_TEMPLATES_IN_A_PATH_WITH_A_BAD_AND_GOOD_YAML = 1
A_PATH_WITH_A_BAD_YAML = 'bad_isp_templates'
A_PATH_WITHOUT_YAML = 'no_isp_templates'
A_NON_EXISTENT_PATH = 'a_non_existent_path'
A_PATH_WITH_A_YAML_FILE_WITH_DUPLICATED_KEYS = 'isp_templates_with_duplicated_keys'
A_PATH_WITH_TWO_YAML_FILES_WITH_DUPLICATED_KEYS = 'isp_templates_with_duplicated_keys_in_files'
A_PATH_INCLUDING_FILES = 'including_files'
COMPLEX_YAML_CONTENT_WITH_INCLUDES = {1: {'key1': 'value1'}, 'default': {'key2': 'value2'}, 0: {'key2': 'value2', 'key0': 'value0'}}


with description('Directory Yaml Loader specs') as self:
    with context('loading all yaml/yml files from folder'):
        with context('when there are yaml files (HappyPath)'):
            with it('retrieves all existing keys'):
                directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_WITH_THREE_YAML))

                templates = directory_yaml_loader.load_all()

                expect(templates.keys()).to(have_length(NUMBER_OF_TEMPLATES_IN_A_PATH_WITH_THREE_YAML))

        with context('when there are some yaml files which are invalid'):
            with context('when a yaml file is an invalid yaml'):
                with it('returns an empty dict'):
                    directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_WITH_A_BAD_YAML))

                    templates = directory_yaml_loader.load_all()

                    expect(templates).to(equal({}))
            with context('when there are invalid and valid yaml file'):
                with it('returns only the keys from valid yaml'):
                    directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_WITH_A_BAD_AND_GOOD_YAML))

                    templates = directory_yaml_loader.load_all()

                    expect(templates.keys()).to(have_length(NUMBER_OF_TEMPLATES_IN_A_PATH_WITH_A_BAD_AND_GOOD_YAML))

        with context('when there are not yaml files'):
            with it('returns an empty dict'):
                directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_WITHOUT_YAML))

                templates = directory_yaml_loader.load_all()

                expect(templates).to(equal({}))

        with context('when the folder path does not exist'):
            with it('returns an empty dict'):
                directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_NON_EXISTENT_PATH))

                templates = directory_yaml_loader.load_all()

                expect(templates).to(equal({}))

        with context('with duplicated keys'):
            with context('when there are duplicated keys at the same file'):
                with it('returns only one key'):
                    directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_WITH_A_YAML_FILE_WITH_DUPLICATED_KEYS))

                    templates = directory_yaml_loader.load_all()

                    expect(templates.keys()).to(have_length(1))

            with context('when there are duplicated keys in different yaml files'):
                with it('raises DuplicatedKeyError'):
                    def _call_directory_yaml_loader_with_duplicated_keys_in_two_files():
                        directory_yaml_loader_to_fail = DirectoryYamlLoader(_absolute_path(A_PATH_WITH_TWO_YAML_FILES_WITH_DUPLICATED_KEYS))

                        directory_yaml_loader_to_fail.load_all()

                    EXPECTED_FILE_NAME = 'duplicated_isp_templates'
                    EXPECTED_KEYS_NAME_DUPLICATED = 'a_duplicated_key'
                    expect(_call_directory_yaml_loader_with_duplicated_keys_in_two_files).to(raise_error(DuplicatedKeyError,
                                                                                                         contain(EXPECTED_FILE_NAME,
                                                                                                                 EXPECTED_KEYS_NAME_DUPLICATED)))

    with context('including files from other files'):
        with it('retrieves all existing keys'):
            directory_yaml_loader = DirectoryYamlLoader(_absolute_path(A_PATH_INCLUDING_FILES))

            templates = directory_yaml_loader.load_all()

            expect(templates).to(equal(COMPLEX_YAML_CONTENT_WITH_INCLUDES))


def _absolute_path(path):
    return f'{BASE_PATH}/{path}'
