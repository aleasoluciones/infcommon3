from infcommon.factory import Factory
from infcommon.serializer.serializers import (
    JsonPickleSerializer,
    JsonSerializer,
    PickleSerializer,
    JsonOrPickleSerializer,
)


def jsonpickle_serializer():
    return Factory.instance('jsonpickle_serializer',
                            lambda: JsonPickleSerializer()
                            )


def json_serializer():
    return Factory.instance('json_serializer',
                            lambda: JsonSerializer()
                            )


def pickle_serializer():
    return Factory.instance('pickle_serializer',
                            lambda: PickleSerializer()
                            )


def json_or_pickle_serializer():
    return Factory.instance('json_or_pickle_serializer',
                            lambda: JsonOrPickleSerializer(json_serializer(),
                                                           pickle_serializer()
                                                           )
                            )


