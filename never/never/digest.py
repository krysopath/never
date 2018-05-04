#!/usr/bin/env python
# coding=utf-8
import binascii
import hashlib
from string import ascii_letters as letters, digits


class PWGen(object):
    def __init__(self, pw):
        self.pw = pw
        self.numbers = {
            0: '?',
            1: '-',
            2: '_',
            3: '~',
            4: '$',
            5: '%',
            6: '&',
            7: '/',
            8: '*',
            9: '#',
        }

    @staticmethod
    def _digest(myseed, mysecret):
        digest = binascii.hexlify(
            hashlib.pbkdf2_hmac(
                'sha512',
                mysecret.encode(),
                myseed.encode(),
                300000
            )
        )
        return digest.decode()

    def _crop(self, _seed, secret, length=16):
        pw = []
        for symbol in self._digest(_seed, secret)[:length]:
            pw.append(symbol)
        return pw

    def _makeseed(self, login):
        return login['_seed'], login['_length']

    def get(self, login):
        pw = []
        _seed, length = self._makeseed(login)
        chars = self._crop(
            _seed,
            self.pw,
            length=int(length)
        )

        for index, symbol in enumerate(chars):
            if symbol in digits:
                if index % 2 == 0:
                    pw.append(
                        self.numbers.get(
                            int(symbol)
                        )
                    )
                else:
                    pw.append(symbol)
            if symbol in letters:
                if not index % 3 == 0:
                    pw.append(symbol)
                else:
                    pw.append(
                        symbol.upper()
                    )
        return ''.join(pw)
