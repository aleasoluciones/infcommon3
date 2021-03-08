import json
import datetime
import pickle

import jsonpickle

from infcommon.serializer.exceptions import DeserializeError


class JsonSerializer:
    def loads(self, serialized_object, **kwargs):
        return json.loads(serialized_object, **kwargs)

    def dumps(self, obj, **kwargs):
        try:
            data = obj.__dict__
        except AttributeError:
            data = obj

        return json.dumps(data, default=_json_serializer, **kwargs)


def _json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return (obj - datetime.datetime(1970, 1, 1)).total_seconds()
    if isinstance(obj, type({}.items())):
        return list(obj)
    return json.JSONEncoder().default(obj)


class PickleSerializer:
    def loads(self, serialized_object, **kwargs):
        return pickle.loads(serialized_object, **kwargs)

    def dumps(self, obj, **kwargs):
        return pickle.dumps(obj, **kwargs)


class JsonOrPickleSerializer:
    def __init__(self, json_serializer, pickle_serializer):
        self._serializers = [json_serializer,
                             pickle_serializer]

    def loads(self, data):
        raised_exception = None
        for serializer in self._serializers:
            try:
                return serializer.loads(data)
            except Exception as exc:
                raised_exception = exc

        raise DeserializeError(raised_exception, data)

    def dumps(self, obj):
        raise NotImplementedError('This serializer should not be used to serialize, only deserialize')


class JsonPickleSerializer:
    def loads(self, serialized_object, **kwargs):
        return jsonpickle.decode(serialized_object, **kwargs)

    def dumps(self, obj, **kwargs):
        return jsonpickle.encode(obj, **kwargs)
