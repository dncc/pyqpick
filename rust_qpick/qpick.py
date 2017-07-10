import os
from .lib import ffi, lib

class QpickResultsIterator(object):
    def __init__(self, ptr, next_fn, free_fn, autom_ptr=None,
                 autom_free_fn=None):
        self._free_fn = free_fn
        self._ptr = ffi.gc(ptr, free_fn)

        self._next_fn = next_fn
        if autom_ptr:
            self._autom_ptr = ffi.gc(autom_ptr, autom_free_fn)
            self._autom_free_fn = autom_free_fn
        else:
            self._autom_ptr = None

    def _free(self):
        # TODO: We could safely free the structures before the GC does,
        #       but unfortunately removing GC-callbacks is only supported
        #       in cffi >= 1.7, which is not yet released.

        # self._free_fn(self._ptr)
        # # Clear GC hook to prevent double-free
        # ffi.gc(self._ptr, None)
        # if self._autom_ptr:
        #     self._autom_free_fn(self._autom_ptr)
        #     ffi.gc(self._autom_ptr, None)
        pass

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        itm = self._next_fn(self._ptr)
        if itm == ffi.NULL:
            self._free()
            raise StopIteration

        qid = itm.qid
        sc = itm.sc
        lib.qpick_item_free(itm)
        return (qid, sc)


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

    def get_as_string(self, query):
        c_str = lib.qpick_get_as_string(self._ptr, query)
        py_str = ffi.string(c_str).decode('utf8')
        lib.string_free(c_str)
        return py_str

    def get(self, query, count=100):
        res_ptr = lib.qpick_get(self._ptr, query, count)
        return QpickResultsIterator(res_ptr,
                                    lib.qpick_iter_next,
                                    lib.qpick_results_free)
