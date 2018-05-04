#!/usr/bin/env python3
# coding=utf-8
import easywebdav as ewd
from itertools import chain
from getpass import getpass

__davconn__ = "g:abcabc@https://premiumtrading.online/safe/remote.php/webdav/"
try:              # Python 2
    str_base = basestring
    items = 'iteritems'
except NameError: # Python 3
    str_base = str, bytes, bytearray
    items = 'items'

def ensure_lower(maybe_str):
    """dict keys can be any hashable object - only call lower if str"""
    return maybe_str.lower() if isinstance(maybe_str, str_base) else maybe_str


class LowerDict(dict):  # dicts take a mapping or iterable as their optional first argument
    __slots__ = () # no __dict__ - that would be redundant

    @staticmethod # because this doesn't make sense as a global function.
    def _process_args(mapping=(), **kwargs):
        if hasattr(mapping, items):
            mapping = getattr(mapping, items)()
        return ((ensure_lower(k), v) for k, v in chain(mapping, getattr(kwargs, items)()))

    def __init__(self, mapping=(), **kwargs):
        super(LowerDict, self).__init__(self._process_args(mapping, **kwargs))

    def __getitem__(self, k):
        return super(LowerDict, self).__getitem__(ensure_lower(k))

    def __setitem__(self, k, v):
        return super(LowerDict, self).__setitem__(ensure_lower(k), v)

    def __delitem__(self, k):
        return super(LowerDict, self).__delitem__(ensure_lower(k))

    def get(self, k, default=None):
        return super(LowerDict, self).get(ensure_lower(k), default)

    def setdefault(self, k, default=None):
        return super(LowerDict, self).setdefault(ensure_lower(k), default)

    def pop(self, k):
        return super(LowerDict, self).pop(ensure_lower(k))

    def update(self, mapping=(), **kwargs):
        super(LowerDict, self).update(self._process_args(mapping, **kwargs))

    def __contains__(self, k):
        return super(LowerDict, self).__contains__(ensure_lower(k))

    @classmethod
    def fromkeys(cls, keys):
        return super(LowerDict, cls).fromkeys(ensure_lower(k) for k in keys)


class AnakinSettings():
    def __init__(self, *args, **kwargs):
        #LowerDict.__init__(self, **kwargs)
        self._username = None
        self._protocol = None
        self._password = None
        self._port = None
        self._host = None
        self._path = None
        self._verify_ssl = True
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.properties = ['username', 'password', 'protocol', 'host', 'path', 'port']

    def __repr__(self):
        try:
            return "{}:**** {}://{}/{} via port {}".format(self.username, self.protocol, self.host, self.path, self.port)
        except TypeError:
            return "empty %s" % type(self)

    def __iter__(self):
        """
        necessary for *arg unpacking into object()
        :return:
        """
        for p in self.properties:
            yield p, getattr(self, p)

    @property
    def username(self):
        return self._user

    @username.setter
    def username(self, v):
        if isinstance(v, str):
            self._user = v
        else:
            raise ValueError

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, v):
        if isinstance(v, str):
            self._password = v
        else:
            raise ValueError

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, v):
        if v in ['http', 'https']:
            self._protocol = v
        else:
            raise ValueError

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, v):
        self._host = v

    @property
    def verify_ssl(self):
        return self._host

    @verify_ssl.setter
    def verify_ssl(self, v):
        if isinstance(v, bool):
            self._verify_ssl = v
        else:
            raise ValueError

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, v):
        self._path = v

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, v):
        if isinstance(v, int) and 0 < v < 65535:
            self._port = int(v)
        else:
            raise ValueError


def uri2settings(uri):
    username, rest = uri.split(':', 1)
    password, rest = rest.split('@', 1)
    protocol, rest = rest.split('://')
    host, path = rest.split('/', 1)
    if protocol == 'http':
        port = 80
    elif protocol == 'https':
        port = 443
    else:
        port = None
    return AnakinSettings({
        'host': host,
        'username': username,
        'password': password,
        'protocol': protocol,
        'path': path,
        'port': port})


class AnakinDAVWalker:
    def __init__(self, *args, **kwargs):
        self.dav = ewd.connect(
            *args,
            **kwargs
        )

    def ls(self, path=''):
        try:
            elements = self.dav.ls(
                remote_path=path
            )
            directories = [element for element in elements if element.contenttype == '']
            files = [element for element in elements if element.contenttype != '']
            d_dirs = {d.name: d for d in directories}
            d_file = {d.name: d for d in files}
            return d_dirs, d_file
        except ewd.client.OperationFailed as of:
            return False, of

    def cd(self, path='.'):
        try:
            self.dav.cd(path)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

    def mkdir(self, name):
        try:
            self.dav.mkdir(name)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

    def put(self, filepath, remotepath):
        try:
            self.dav.upload(filepath, remotepath)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

    def get(self, remotepath, filepath):
        try:
            self.dav.download(remotepath, filepath)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

    def rmdir(self, path):
        try:
            self.dav.rmdir(dir, path)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

    def rm(self, path):
        try:
            self.dav.delete(path)
            return True
        except ewd.client.OperationFailed as of:
            return False, of

if __name__ == "__main__":
    s = uri2settings(__davconn__)
    s.password = getpass('davpw:')
    for p in s:
        print(p)


    walker = AnakinDAVWalker(
        **dict(s)
    )
    print(walker.ls())
    walker.cd('never.backup')
    print(walker.ls())
    walker.put('__init__.py', 'i.py')











