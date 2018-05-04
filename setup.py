#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

required_foreign = []  # ['asciimatics', 'urwid']
required_own = ['anakin', ]  # 'tbx_dbio>=0.3.1.2']
setup(
    name='never',
    version='0.2.1.1',
    description='remote access db of seeds to get a password from digested seeds.',
    url='ssh://git@endtropie.mooo.com:22222/home/git/never.git',
    author='Georg',
    author_email='krysopath@gmail.com',
    license='GPL',
    packages=['never'],
    scripts=[
        'broker',
        'ascii',
    ],
    install_requires=required_foreign + required_own,
    zip_safe=False
)
