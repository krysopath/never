#!/usr/bin/env python3
# coding=utf-8
from tbx_dbio.sql import DBTable


class Constraints:
    def __init__(self):
        pass

    def make(self):
        return


class DataSet:
    schema = {}

    def __init__(self, *initial_data, **kwargs):
        self.__data__ = set()

        schema = type(self).schema
        for key in schema:
            self.__data__.add(key)
            setattr(self, key, None)

        for dictionary in initial_data:
            for key in dictionary:
                self.__data__.add(key)
                setattr(self, key, dictionary[key])

        for key in kwargs:
            self.__data__.add(key)
            setattr(self, key, kwargs[key])

    def __iter__(self):
        for p in self.__data__:
            yield p, self.__getattribute__(p)

    def __str__(self):
        return ",\n".join(
            ['{}: {}'.format(kv[0], kv[1])
             for kv in self
             ]
        )

    def __getitem__(self, item):
        if item in self.__data__:
            return getattr(self, item)

    def add(self, item):
        if not hasattr(self, item) and \
                        item not in self.__data__:
            self.__data__.add(item)
            setattr(self, item, None)

    def remove(self, item):
        if hasattr(self, item) and \
                        item in self.__data__:
            self.__data__.remove(item)
            delattr(self, item)


class LibraryData(DataSet):
    schema = {
        _name: type(_type)
        for _name, _type
        in DBTable.library_schema
    }

    def __init__(self, *initial_data, **kwargs):
        super(LibraryData, self).__init__(*initial_data, **kwargs)


class LoginData(DataSet):
    schema = {_name: type(_type) for _name, _type in DBTable.login_schema}

    def __init__(self, *initial_data, **kwargs):
        super(LoginData, self).__init__(*initial_data, **kwargs)

