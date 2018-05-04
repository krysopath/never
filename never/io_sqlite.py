#!/usr/bin/env python3
# coding=utf-8
import sqlite3 as sql
from collections import OrderedDict
from json import loads, dumps


class DBTable:
    never_schema = (
        ('login', ''),
        ('lgroup', ''),
        ('link', ''),
        ('username', ''),
        ('email', ''),
        ('notes', ''),
        ('seed', ''),
        ('length', 1)
    )
    login_schema = (
        ('login', ''),
        ('hash', ''),
        ('since', 1)

    )
    default = never_schema

    def __init__(self, givenname, givenfields=None):
        print('table_init')
        if not givenfields:
            givenfields = DBTable.default
        self.types = (int, str, tuple, dict)
        self.fields = OrderedDict()
        assert isinstance(givenfields, tuple)
        assert isinstance(givenname, str)
        assert '-' not in givenname

        for field in givenfields:
            _name, _type = field
            assert isinstance(
                _type,
                self.types
            )
            if isinstance(_type, (str, dict, tuple,)):
                self.fields[_name] = "TEXT"

            elif isinstance(_type, int):
                self.fields[_name] = "INTEGER"

        self.name = givenname

    def _add_field(self, field):
        _name, _type = field
        assert isinstance(field, tuple)
        assert isinstance(_name, str)
        assert isinstance(_type, str)
        self.fields[_name] = _type

    def _create(self, overwrite=False):
        if overwrite:
            _sql = """DROP TABLE IF EXISTS {0}; CREATE TABLE {0} (id INTEGER PRIMARY KEY AUTOINCREMENT, %s);""" \
                .format(self.name)
        else:
            _sql = """CREATE TABLE {0} (id INTEGER PRIMARY KEY AUTOINCREMENT, %s);""".format(self.name)

        return _sql % ', '.join(
            ['%s %s NOT NULL' %
             (name, self.fields[name])
             for name in self.fields]
        )

    def _get(self, criterion, returnfields=None):
        if not returnfields:
            returnfields = '*'
        return """SELECT {0} FROM {1} WHERE {2}=?;""".format(
            returnfields, self.name, criterion)

    def _remove(self, criterion):
        return """DELETE FROM {0} WHERE {1}=?;""".format(
            self.name, criterion
        )

    def _getsummary(self, returnfields=None):
        if not returnfields:
            returnfields = '*'
        return """SELECT {0} FROM {1};""".format(
            returnfields, self.name)

    def _insert(self):
        _sql = """INSERT INTO {0} (%s) VALUES (%s);""".format(self.name)
        fields = ', '.join([name for name in self.fields])
        wildcards = ', '.join([':%s' % name for name in self.fields])
        return _sql % (fields, wildcards)

    def _update(self):
        _sql = """UPDATE {0} SET %s WHERE id=:id;""".format(self.name)
        wildcards = ', '.join(['%s=:%s' % (name, name) for name in self.fields])
        return _sql % wildcards

    def _del_rst_where_x(self, criterion, condition):
        _sql = """DELETE FROM {0} WHERE {1}='%s';""".format(self.name, criterion)
        return _sql % condition

    def _filtered_summary(self, where, returnfields='*'):
        _sql = """SELECT {0} FROM {1} WHERE {2} LIKE ?;""".format(returnfields, self.name, where)
        return _sql


class DataModel(DBTable):
    def __init__(self, name, fields=None, db=':memory:'):
        print('datamodel_init')
        DBTable.__init__(self, givenname=name, givenfields=fields)
        print('connecting %s' % db)
        self._db = sql.connect(db)
        self._db.row_factory = sql.Row

        # Current row when editing.
        self.current_id = None

    def create(self, overwrite=False):
        # Create the basic contact table.
        """
        '''
           CREATE TABLE logins(
               id INTEGER PRIMARY KEY,
               login TEXT NOT NULL,
               lgroup TEXT NOT NULL,
               link TEXT NOT NULL,
               username TEXT NOT NULL,
               email TEXT,
               notes TEXT,
               seed TEXT NOT NULL)
        '''
        :return:
        """
        self._db.cursor().execute(
            self._create(overwrite=overwrite)
        )
        self._db.commit()

    def add(self, contact):
        self._db.cursor().execute(
            self._insert(),
            contact
        )
        self._db.commit()

    def get_summary(self, select='*'):
        """
        "SELECT * from logins;"
        :return:
        """
        return self._db.cursor().execute(
            self._getsummary(select)
        ).fetchall()

    def get_row(self, _id, select='*', where='id'):
        return self._db.cursor().execute(
            self._get(where, select), str(_id)
        ).fetchone()

    def get_filter_summary(self, where, like, returnfields='*'):
        """
        "SELECT login, id from logins WHERE lgroup LIKE ?", '%{}%'.format(str(lgroup))
        :param lgroup:
        :return:
        """
        return self._db.cursor().execute(
            self._filtered_summary(where, returnfields),
            ('%{}%'.format(str(like)),)
        ).fetchall()

    def get_current_row(self):
        if self.current_id is None:
            return {}
        else:
            return self.get_row(self.current_id)

    def update_current_row(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self.update_row(details)
            self._db.commit()

    def update_row(self, details):
        self._db.cursor().execute(
            self._update(),
            details
        )
        self._db.commit()

    def delete_row(self, _id):
        self._db.cursor().execute('''
            DELETE FROM logins WHERE id=:id''', {"id": _id})
        self._db.commit()


def setup(table, _dbfile=':memory:'):
    print('recreating db...')

    with sql.connect(_dbfile) as con:
        cur = con.cursor()
        cur.executescript(
            table._create()
        )
        con.commit()


def put_login_to_db(recordset, _dbfile=':memory:'):
    assert isinstance(recordset, tuple)
    with sql.connect(_dbfile) as con:
        cur = con.cursor()
        login, seed = recordset
        cur.execute(
            table._insert(),
            (login, dumps(seed),)
        )
        con.commit()


def get_login_from_db(login, _dbfile=':memory:'):
    assert isinstance(login, str)
    _sql = table._get('login')
    with sql.connect(_dbfile) as con:
        cur = con.cursor()
        cur.execute(_sql, (login,))

        try:
            l_data = loads(
                cur.fetchone()[2]
            )
            return {
                'random': l_data[0],
                'account': l_data[1],
                'length': l_data[2],
                'username': l_data[3],
                'link': l_data[4]
            }
        except TypeError as te:
            return None


def get_all_logins(_dbfile=':memory:'):
    _sql = 'SELECT * FROM tbx_never_stash;'
    with sql.connect(_dbfile) as con:
        cur = con.cursor()
        cur.execute(_sql)
        return cur.fetchall()


def check_existant(login, _dbfile=':memory:'):
    results = get_login_from_db(login, _dbfile=_dbfile)
    if results:
        return True
    else:
        return False


def add_login_to_db(login, db=':memory:'):
    def assert_type(_type, x):
        try:
            assert isinstance(x, _type)
            return True
        except AssertionError:
            return False

    if not check_existant(login, db):
        if len(login) == 0:
            print('error: empty name')
            return False
        print("the following userinputs are to seed the hash and should" + \
              " not be changed, else you are going to break working logins")
        randomstuff = input('give me some random info: ')
        account = login
        username = input('your username: ')
        loginlink = input('login via this link: ')
        length = input('length of password: ')

        info = (randomstuff, account, length, username, loginlink)

        put_login_to_db((login, info,), _dbfile=db)
        return True
    print(login, 'already in', table.name)
    return False


def del_login_from_db(login, _dbfile=':memory:'):
    if check_existant(login, _dbfile):
        print('deleting %s from db' % login)
        if not input('_remove %s y/n?' % login) == 'y':
            return
        _sql = table._del_rst_where_x('login', login)
        with sql.connect(_dbfile) as con:
            cur = con.cursor()
            cur.execute(_sql)
            con.commit()


def backup(_dbfile, topath):
    """
    shutil.copy(filepath, targetdir)
    :param _dbfile: path to a readable file
    :param topath: path to a writable directory
    :return:
    """
    print('\n(saving db...)')
    try:
        copy(
            _dbfile,
            topath + basename(_dbfile) + '.last'
        )
    except PermissionError as pe:
        print('!!!not permitted to write', pe.args[1])
    except OSError as oe:
        print('!!!unable to access', oe.args[1])
