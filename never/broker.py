#!/usr/bin/env python3
# coding=utf-8
from collections import OrderedDict
from datetime import datetime
from getpass import getpass
from os import mkdir, environ
from os.path import exists
from random import SystemRandom
from string import ascii_letters as letters, digits

import never.io_sqlite as dbio
from never.digest import PWGen

# import anakin as dav, für backup über webdav
dav = None

__author__ = "Georg vom Endt"
__email__ = "krysopath@gmail.com"
__license__ = """Copyright (c) 2016 Georg vom Endt <krysopath@gmail.com>"""
#__stash__ = '{}//stash//'.format(environ['HOME'])
__stash__ = '{}/.never/'.format(environ['HOME'])
__dbfile__ = __stash__ + '%s/%s.db'


class NeverUserHelp:
    help = OrderedDict(
        {'_login': 'enter a name to remember this\n..',
         '_group': 'the group for sorting\n..',
         '_username': 'the username on the page\n..',
         '_email': 'an associated email\n..',
         '_link': 'the link to reach the ressource\n..',
         '_notes': 'additional notes\n..',
         '_length': 'length of derived passwort\n..'}
    )


class NeverModel(dbio.DataModel):
    schema = (
        ('_login', ''),
        ('_group', ''),
        ('_link', ''),
        ('_username', ''),
        ('_email', ''),
        ('_notes', ''),
        ('_seed', ''),
        ('_length', 1)
    )
    names = [name[0] for name in schema]

    def __init__(self, tablename, schema, dbpath):
        super(NeverModel, self).__init__(tablename, schema, dbpath)


class NeverDataSet(dbio.DataSet):
    schema = {_name: type(_type)
              for _name, _type
              in NeverModel.schema}

    def __init__(self, *initial_data, **kwargs):
        super(NeverDataSet, self).__init__(*initial_data, **kwargs)
        self.shorten = True
        self.lock_seed = False
        self.mask_seed = True

    def create_seed(self):
        if hasattr(self, '_seed') and not self._seed:
            self.__data__.add('_seed')
            setattr(self, '_seed', self.__seed_gen())
            return True
        else:
            return False

    @staticmethod
    def __seed_gen(
            size=128,
            chars=letters + digits):
        return ''.join(
            SystemRandom().choice(chars)
            for _ in range(size)
        )

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email:
            try:
                name, fqdn = email.split('@')
                host, country = fqdn.split('.')
                self._email = email
            except ValueError as e:
                raise ValueError('Thou shall not apply bad input to email!')
        else:
            self._email = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login):
        if not login:
            raise ValueError('Thou need a valid login!')
        if all([x in letters+digits for x in login]):
            self._login = login

    @property
    def seed(self):
        if self.mask_seed:
            return '******'
        elif self.shorten:
            return self._seed[:16]
        else:
            return self._seed

    @seed.setter
    def seed(self, value):
        if self.lock_seed:
            raise ValueError('Thou may not change thy seed')
        else:
            self._seed = value

    @property
    def group(self):
        return self._group

    @property
    def link(self):
        return self._link

    @property
    def username(self):
        return self._username

    @property
    def notes(self):
        return self._notes

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not isinstance(value, int):
            raise ValueError('length needs to be an integer..')
        if not 4 <= value <= 255:
            raise ValueError('length needs to be between 4 and 255, arbitrarily..')
        self._length = value


class Interactor:
    def __init__(self, for_user, master_pw):
        self.user = for_user
        self.pwgen = PWGen(master_pw)
        self.db = NeverModel(
            'logins',
            NeverModel.schema,
            __dbfile__ % (self.user, self.user)
        )
        try:
            self.db.create()
        except Exception as e:
            print('(dont need to create table, because)')
            print('(%s)' % e)

    def make_pw(self, data):
        return self.pwgen.get(data)

    def add_login(self, login=None):
        def askfor(k):
            try:
                value = NeverDataSet.schema[k](
                    input(
                        "%s: %s>" % (k, NeverUserHelp.help[k])
                    )
                )
                if k in ['_login',
                         '_username',
                         '_group',
                         '_link',
                         '_email']:
                    if not value:
                        raise ValueError
            except ValueError:
                print(k, 'is a obligatory', NeverDataSet.schema[k])
                value = askfor(k)

            return value

        user = {
            k: v for k, v
            in NeverUserHelp.help.items()
        }
        if login:
            user['_login'] = login

        for k, v in user.items():
            user[k] = askfor(k)

        nds = NeverDataSet(**user)
        nds.create_seed()
        self.db.add(
            dict(nds)
        )

    def del_login(self, login=None):
        if not login:
            login = input('login>')
        self.db.delete_row_where('_login', login)

    def get_login(self, login=None):
        if not login:
            login = input('login>')
        data = self.db.get_row(
            where='_login', equals=login
        )
        if data:
            nds = NeverDataSet(
                **data
            )
            nds.lock_seed = True
            nds.add('password')
            nds.password = self.pwgen.get(nds)
            nds.mask_seed = True
            return nds
        else:
            print('none found')
            return None

    def list_logins(self, filter=None):
        if not filter:
            out = self.db.get_summary(
                select='_login, _username, _link, _email, _group'
            )
        else:
            out = self.db.get_filter_summary(
                select='_login, _username, _link, _email',
                where='_group', like=filter
            )
        return [NeverDataSet(**result) for result in out if result]

    def filter(self, where=None):
        def askfor_where():
            print(
                '(possible fields: %s)'
                % ', '.join(
                    NeverModel.names
                )
            )
            where = input('search in>')
            if where in NeverModel.names:
                return where
            else:
                askfor_where()

        if not where:
            where = askfor_where()
        else:
            if where not in NeverModel.names:
                print('invalid field')
                where = askfor_where()

        like = input('search for>')

        if all([where, like]):
            results = [
                NeverDataSet(**result)
                for result in
                self.db.get_filter_summary(
                    select='_id, _login, _group',
                    where=where, like=like
                ) if result]
            return results

        else:
            print(
                '(consider adding search expression when using filter...)'
            )
            return None

    def backup(self, arg=None):
        settings = dav.uri2settings(dav.__davconn__)
        settings.password = getpass('shared secret for dav access>')

        b = dav.AnakinDAVWalker(**dict(settings))
        b.cd('never.backup')
        b.put(
            self.db.path,
            'never_{}-{}.db'.format(
                self.user,
                datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            )
        )
        return None

    def modify_login(self, login=None):
        pass


def dir_setup(stash_dir, user):
    path = '{}/{}'.format(stash_dir, user)
    if not exists(stash_dir):
        print('(creating folderstructure..)')
        mkdir(stash_dir)
    else:
        print('(all good)')
    if not exists(path):
        mkdir(path)
