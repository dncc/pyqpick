import os
from .lib import ffi, lib

class Qpick(object):
    def __init__(self, dir_path=None, _pointer=None):
        """Loads a query index from a given directory.

        :param dir_path:    Directory path to index on disk
        """
        # self._ctx = ffi.gc(lib.qpick_context_new(), lib.qpick_context_free)

        if dir_path:
            if not os.path.isdir(dir_path):
                raise Exception("%s is not a directory!" % dir_path)

            # returns a pointer to rust Qpick struct
            s = lib.qpick_init(dir_path)
        else:
            s = _pointer

        self._ptr = ffi.gc(s, lib.qpick_free)

    def search(self, query):
        c_str = lib.qpick_search(self._ptr, query)
        py_str = ffi.string(c_str).decode('utf8')
        lib.string_free(c_str)
        return py_str
