#!/usr/bin/env python3
# coding=utf-8
import pprint
import readline
from getpass import getpass
from os import environ
from sys import argv

from never.broker import dir_setup, Interactor
from never.exceptions import EndInputLoop
from never.io_sqlite import backup


class SimpleCompleter:
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [
                    s for s in self.options
                    if s and s.startswith(text)
                    ]

            else:
                self.matches = self.options[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        # logging.debug('complete(%s, %s) => %s',
        #              repr(text), state, repr(response))
        return response


def stop(reasons=''):
    backup(i.db.path, __backuppath__)
    print('never.broker ending because %s..' % reasons)
    exit(0)


def show(nds):
    message = """
\t_login:      {}
\t_group:      {}
\t_username:   {}
\t_password:   {}
\t_length:     {}
\t_link:       {}
\t_email:      {}
\t_seed:       {}
\t_notes:      {}
    """.format(
        nds.login, nds.group,
        nds.username, nds.password,
        nds.length, nds.link,
        nds.email, nds.seed,
        nds.notes
    )
    print(message)


def summary(listof_nds):
    for result in listof_nds:
        print(
            """
\t_login: {},
\t_group: {}
\t_email: {},
\t_username: {},
\t_link: {}\n""".format(
                result.login,
                result.group,
                result.email,
                result.username,
                result.link
            )
        )


def startup():
    print('(running never.broker)')
    print('(validated user %s by ssh)' % user)
    print('(backup in %s)' % __backuppath__)
    print("(type stop to quit and use tab for auto-completion)")


def input_loop():
    line = ''
    while True:
        line = input('never> ')
        try:
            cmd, args = None, None
            cmd, args = line.split(' ', 1)
        except ValueError:
            cmd, args = line, ''
        finally:
            pass

        if cmd in commands:
            func = commands_d[cmd]
            try:
                out = None
                if args:
                    out = func(args)
                else:
                    out = func()
            except Exception as e:
                raise e
            finally:
                if out:
                    if isinstance(out, list):
                        summary(out)
                    else:
                        show(out)

                out = None
        elif line != '' and not line == 'stop':
            print('%s: not found..' % line)
        elif line == 'stop':
            raise EndInputLoop


if __name__ == '__main__':
    readline.parse_and_bind('tab: complete')
    __stash__ = '{}//stash//'.format(environ['HOME'])
    masterpw = getpass('input master pw? ')
    user, __backuppath__ = argv[1], argv[2]
    dir_setup(__stash__, user)
    i = Interactor(user, masterpw)
    pp = pprint.PrettyPrinter(indent=8)

    commands_d = {
        'add': i.add_login,
        'get': i.get_login,
        'list': i.list_logins,
        'modify': i.modify_login,
        'del': i.del_login,
        'filter': i.filter,
        'backup': i.backup
    }
    commands = [cmd for cmd in commands_d.keys()]
    readline.set_completer(
        SimpleCompleter(commands).complete
    )
    startup()
    reason = None

    try:
        input_loop()
    except EndInputLoop:
        reason = 'user entered stop'
    except EOFError:
        reason = 'user entered strg+c in input()'
    except KeyboardInterrupt:
        reason = 'user entered strg+c'
    except Exception as e:
        reason = e.args[1]
        raise e
    finally:
        stop(reason)
