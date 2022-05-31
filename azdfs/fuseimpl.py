#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations, fuse_get_context
import inspect

def removeself(dict):
    dict.pop('self', None)
    return dict

class Impl(Operations):
    def __init__(self, root, dict):
        self.root = root
        self.dict=dict

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def chmod(self, path, mode):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def chown(self, path, uid, gid):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def getattr(self, path, fh=None):

        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def readdir(self, path, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def readlink(self, path):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def mknod(self, path, mode, dev):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def rmdir(self, path):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def mkdir(self, path, mode):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def statfs(self, path):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def unlink(self, path):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def symlink(self, name, target):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def rename(self, old, new):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def link(self, target, name):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def utimens(self, path, times=None):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    # File methods
    # ============

    def open(self, path, flags):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def create(self, path, mode, fi=None):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def read(self, path, length, offset, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def write(self, path, buf, offset, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def truncate(self, path, length, fh=None):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def flush(self, path, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def release(self, path, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

    def fsync(self, path, fdatasync, fh):
        print(f"{inspect.stack()[0][3]}({removeself(locals())}): not implemented")

def createFUSE(*, mountpoint, dict):
    FUSE(Impl(mountpoint, dict), mountpoint, nothreads=True, foreground=True, allow_other=True)
