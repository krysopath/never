#!/usr/bin/env python3
# coding=utf-8
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene

from broker.ascii_views import LoginView, ListView, ContactView
from dbio import DataModel

import sys
from os import environ, mkdir
from os.path import exists


__masterpw__ = None
__stash__ = '{}//stash//'.format(environ['HOME'])
__dbfile__ = __stash__ + '%s.db'


class ConfirmPassword(LoginView):
    def __init__(self, screen):
        super(ConfirmPassword, self).__init__(screen)

    def _ok(self):
        if self._pw1.value == self._pw2.value \
                and not self._pw1 == '':
            global __masterpw__
            __masterpw__ = self._pw1.value
            raise NextScene("Main")


class NeverDataModel(DataModel):
    def __init__(self, path=':memory:'):
        self.filepath = path
        super(NeverDataModel, self).__init__(
            name='logins',
            fields=NeverDataModel.never_schema,
            db=self.filepath
        )




def demo(screen, scene):
    scenes = [
        Scene([ConfirmPassword(screen)], -1, name="Login"),
        Scene([ListView(screen, loginstash)], -1, name="Main"),
        Scene([ContactView(screen, loginstash)], -1, name="Edit Login")
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene)


def run():
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

if __name__ == "__main__":
    if not exists(__stash__):
        mkdir(__stash__)

    username, mode = sys.argv[1], sys.argv[2]
    filepath = __dbfile__ % username
    loginstash = NeverDataModel(filepath)
    run()
