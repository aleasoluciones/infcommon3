# -*- coding: utf-8 -*-

from mamba import description, before, context, it, _context
from expects import expect, equal, raise_error, have_property, contain
from doublex import Spy, when, ANY_ARG

import json
import jsonpickle
import pickle
import datetime


from infcommon.serializer.serializers import (
    JsonSerializer,
    PickleSerializer,
    JsonOrPickleSerializer,
    JsonPickleSerializer,
)
from infcommon.serializer.exceptions import DeserializeError



A_SIMPLE_DATA = {
    'name': 'event name',
    'data': 'event data',
    'network': 'event network',
}


with description('JsonSerializer') as self:
    with before.each:
        self.serializer = JsonSerializer()

    with context('when serializing to json'):
        with it('returns a json'):
            serialized = self.serializer.dumps(A_SIMPLE_DATA)

            expect(json.loads(serialized)).to(equal(A_SIMPLE_DATA))

    with context('when deserializing datetime'):
        with it('returns the expected data'):
            t = datetime.datetime(2015, 5, 13, 12, 50, 19)
            t_timestamp_format = 1431521419

            serialized = self.serializer.dumps(t)

            expect(json.loads(serialized)).to(equal(t_timestamp_format))


with description('JsonOrPickleSerializer'):
    with context('deserializing/decoding'):
        with context('Happy path'):
            with context('first try to deserialize from json'):
                with it('returns the expected data'):
                    self.real_json_serializer = JsonSerializer()
                    self.real_pickle_serializer = PickleSerializer()
                    self.sut = JsonOrPickleSerializer(self.real_json_serializer,
                                                      self.real_pickle_serializer)
                    a_json_data = self.real_json_serializer.dumps(A_SIMPLE_DATA)

                    deserialized = self.sut.loads(a_json_data)

                    expect(deserialized).to(equal(A_SIMPLE_DATA))

                with context('when deserialize from json fails'):
                    with context('at last try to deserialize from pickle'):
                        with it('returns the expected data'):
                            self.a_spy_json_serializer = Spy(JsonSerializer)
                            self.real_pickle_serializer = PickleSerializer()
                            self.sut = JsonOrPickleSerializer(self.a_spy_json_serializer,
                                                              self.real_pickle_serializer)
                            when(self.a_spy_json_serializer).loads(ANY_ARG).raises(TypeError)
                            a_pickle_data = self.real_pickle_serializer.dumps(A_SIMPLE_DATA)

                            deserialized = self.sut.loads(a_pickle_data)

                            expect(deserialized).to(equal(A_SIMPLE_DATA))

        with context('Object cannot be deserialized json neither pickle (unhappy path'):
            with it('raises a DeserializeError'):
                self.a_spy_json_serializer = Spy(JsonSerializer)
                self.a_spy_pickle_serializer = Spy(PickleSerializer)
                self.sut = JsonOrPickleSerializer(self.a_spy_json_serializer,
                                                  self.a_spy_pickle_serializer)
                when(self.a_spy_json_serializer).loads(ANY_ARG).raises(TypeError)
                when(self.a_spy_pickle_serializer).loads(ANY_ARG).raises(pickle.UnpicklingError)


                def _when_serializer_loads_fails():
                    self.sut.loads('foobar')

                expect(_when_serializer_loads_fails).to(raise_error(DeserializeError,
                                                                   have_property('data', 'foobar')))

    with context('serializing/encoding'):
        with it('raises a NotImplementedError'):
            self.real_json_serializer = JsonSerializer()
            self.real_pickle_serializer = PickleSerializer()
            self.sut = JsonOrPickleSerializer(self.real_json_serializer,
                                              self.real_pickle_serializer)

            def _trying_to_serialize():
                self.sut.dumps('foobar')

            expect(_trying_to_serialize).to(raise_error(NotImplementedError,
                                                        contain('This serializer should not be used to serialize, only deserialize')))


with description('JsonPickleSerializer'):
    with before.each:
        self.serializer = JsonPickleSerializer()

    with context('when serializing/coding to jsonpickle'):
        with it('returns a jsonpickle'):
            serialized = self.serializer.dumps(A_SIMPLE_DATA)

            expect(jsonpickle.decode(serialized)).to(equal(A_SIMPLE_DATA))

    with context('when deserializing/decoding from jsonpickle'):
        with it('returns the expected data'):
            data = A_SIMPLE_DATA
            t = datetime.datetime(2015, 5, 13, 12, 50, 19)
            data['timestamp'] = t
            serialized_data = self.serializer.dumps(data)

            deserialized_data = self.serializer.loads(serialized_data)

            expect(deserialized_data).to(equal(data))
