# -*- coding: utf-8 -*-

import os
import yaml
import tempfile

from mamba import description, context, it, before, after
from expects import expect, equal, be, be_an, raise_error, be_true, be_false

from infcommon.yaml_reader.yaml_reader import YamlReader, YamlReaderNotValidFileError
from infcommon.info_container.info_container import InfoContainer


KEY = 'key'
VALUE = 'value'
NON_EXISTING_KEY = 'non_existing_key'
A_TRUE_BOOLEAN_PARAMETER = 'a_true_boolean_parameter'
A_FALSE_BOOLEAN_PARAMETER = 'a_false_boolean_parameter'
A_TRUE_BOOLEAN_PARAMETER_VALUE = True
A_FALSE_BOOLEAN_PARAMETER_VALUE = False


YAML_CONTENT = {KEY: VALUE,
                A_TRUE_BOOLEAN_PARAMETER: A_TRUE_BOOLEAN_PARAMETER_VALUE,
                A_FALSE_BOOLEAN_PARAMETER: A_FALSE_BOOLEAN_PARAMETER_VALUE,}

with description('YamlReader') as self:
    def _generate_file_and_return_name(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as keyvalue_file:
            keyvalue_file.write(yaml.dump(YAML_CONTENT))
            return keyvalue_file.name

    def _generate_invalid_file_and_return_name(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as keyvalue_file:
            keyvalue_file.write('unbalanced blackets: ]')
            return keyvalue_file.name

    def _generate_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as keyvalue_file:
            return keyvalue_file.name

    with context('given an invalid yaml file'):
        with fit('raises Exception'):
            invalid_yaml_file = self._generate_invalid_file_and_return_name()
            invalid_yaml_reader = YamlReader(invalid_yaml_file)

            def _accesing_attribute_from_invalidad_yaml_file():
                invalid_yaml_reader[KEY]

            expect(_accesing_attribute_from_invalidad_yaml_file).to(raise_error(YamlReaderNotValidFileError))

            os.unlink(invalid_yaml_file)

    with context('given a valid yaml file'):

        with before.all:
            self.yaml_file = self._generate_file_and_return_name()
            self.yaml_reader = YamlReader(self.yaml_file)

        with after.all:
            os.unlink(self.yaml_file)

        with context('given a yaml file'):
            with context('when obtaining an info container'):
                with it('returns an info container'):
                    result = self.yaml_reader.get_info_container()

                    expect(result).to(be_an(InfoContainer))

                with it('contains keyvalues from yaml file'):
                    result = self.yaml_reader.get_info_container()

                    expect(result).to(equal(InfoContainer({KEY: VALUE,
                                                           A_TRUE_BOOLEAN_PARAMETER: A_TRUE_BOOLEAN_PARAMETER_VALUE,
                                                           A_FALSE_BOOLEAN_PARAMETER: A_FALSE_BOOLEAN_PARAMETER_VALUE,}, return_none=True)))

        with context('given a yaml_reader object with properties loaded in it'):
            with context('when accesing an attribute'):
                with context('that exists'):
                    with it('returns its value'):
                        expect(self.yaml_reader[KEY]).to(equal(VALUE))

                with context('that does NOT exist'):
                    with it('raises a KeyError exception'):
                        def accesing_a_non_existing_attribute():
                            self.yaml_reader[NON_EXISTING_KEY]

                        expect(accesing_a_non_existing_attribute).to(raise_error(KeyError))

            with context('when getting a value from a key'):
                with context('that exists'):
                    with it('returns its value'):
                        expect(self.yaml_reader.get(KEY)).to(equal(VALUE))

                    with context('when parameter value is boolean'):
                        with context('when parameter value is True'):
                            with it('returns the value correctly'):
                                result = self.yaml_reader.get(A_TRUE_BOOLEAN_PARAMETER)

                                expect(result).to(be_true)

                        with context('when parameter value is False'):
                            with it('returns the value correctly'):
                                result = self.yaml_reader.get(A_FALSE_BOOLEAN_PARAMETER)

                                expect(result).to(be_false)


                with context('that does NOT exist'):
                    with it('returns None'):
                        expect(self.yaml_reader.get(NON_EXISTING_KEY)).to(be(None))

            with context('when getting a key from a value'):
                with context('that exists'):
                    with it('returns the key for the first matching value'):
                       result = self.yaml_reader.get_key_by(value=VALUE)

                       expect(result).to(equal(KEY))

            with context('when getting all the content'):
                with context('having yaml content'):
                    with it('returns content'):
                        all_content = self.yaml_reader.get_all()

                        expect(all_content).to(equal(YAML_CONTENT))
