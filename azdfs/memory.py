#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

import inspect
from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from refuse.high import FUSE, FuseOSError, Operations, LoggingMixIn

if not hasattr(__builtins__, 'bytes'):
    bytes = str


class Memory(LoggingMixIn, Operations):
    'Example memory filesystem. Supports only one level of files.'

    def __init__(self, fsDict):
        self.files = fsDict
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
        self.files['/'] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)

    def chmod(self, path, mode):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.files[path]['st_mode'] &= 0o770000
        self.files[path]['st_mode'] |= mode
        return 0

    def chown(self, path, uid, gid):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid

    def create(self, path, mode):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.files[path] = dict(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time())

        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]

    def getxattr(self, path, name, position=0):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        attrs = self.files[path].get('attrs', {})

        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR

    def listxattr(self, path):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()

    def mkdir(self, path, mode):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.files[path] = dict(
            st_mode=(S_IFDIR | mode),
            st_nlink=2,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time())

        self.files['/']['st_nlink'] += 1

    def open(self, path, flags):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        return self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        return ['.', '..'] + [x[1:] for x in self.files if x != '/']

    def readlink(self, path):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        return self.data[path]

    def removexattr(self, path, name):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        attrs = self.files[path].get('attrs', {})

        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR

    def rename(self, old, new):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.data[new] = self.data.pop(old)
        self.files[new] = self.files.pop(old)

    def rmdir(self, path):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        # with multiple level support, need to raise ENOTEMPTY if contains any files
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1

    def setxattr(self, path, name, value, options, position=0):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value

    def statfs(self, path):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.files[target] = dict(
            st_mode=(S_IFLNK | 0o777),
            st_nlink=1,
            st_size=len(source))

        self.data[target] = source

    def truncate(self, path, length, fh=None):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        # make sure extending the file fills in zero bytes
        self.data[path] = self.data[path][:length].ljust(
            length, '\x00'.encode('ascii'))
        self.files[path]['st_size'] = length

    def unlink(self, path):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.data.pop(path)
        self.files.pop(path)

    def utimens(self, path, times=None):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        logging.debug(f"{inspect.stack()[0][3]}, dict: {self.files.items()}")
        self.data[path] = (
            # make sure the data gets inserted at the right offset
                self.data[path][:offset].ljust(offset, '\x00'.encode('ascii'))
                + data
                # and only overwrites the bytes that data is replacing
                + self.data[path][offset + len(data):])
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)



def createFUSE(*, mountpoint, fsDict):
    FUSE(Memory(fsDict), mountpoint, nothreads=True, foreground=True, allow_other=True)