# -*- coding: utf-8 -*-

import pprint


class InfoContainer(object):

    def __init__(self, items, return_none=False):
        self.__items = []
        self.__data = items
        self.return_none = return_none

        if isinstance(items, dict):
            self.__items.append({})
            for key, value in items.items():
                self.__items[0][key] = self._convert_to_info_container_if_needed(value)
        if isinstance(items, (list, tuple)):
            for value in items:
                self.__items.append(self._convert_to_info_container_if_needed(value))

    def data(self):
        return self.__data

    def is_list(self):
        return len(self.__items) > 0 and isinstance(self.__items[0], self.__class__)

    def _convert_to_info_container_if_needed(self, value):
        if isinstance(value, dict):
            return self.__class__(value, return_none=self.return_none)
        if isinstance(value, (list, tuple)):
            return [self._convert_to_info_container_if_needed(elem) for elem in value]
        return value

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__items[key]
        return self.__items[0][key]

    def __len__(self):
        return len(self.__items)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            try:
                return self.__items[0][name]
            except KeyError:
                if self.return_none:
                    return None
                raise AttributeError(name)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state
