#!/usr/bin/env python3
# coding=utf-8
from setuptools import setup

setup(
    name='anakin',
    version='0.1.1.1',
    description='webdav classes',
    url='ssh://git@endtropie.mooo.com:22222/home/git/anakin.git',
    author='Georg',
    author_email='krysopath@gmail.com',
    license='GPL',
    packages=['anakin', 'easywebdav'],
    install_requires=['requests'],
    zip_safe=False
)
