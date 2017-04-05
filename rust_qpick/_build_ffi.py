from cffi import FFI

ffi = FFI()
ffi.set_source('rust_qpick._ffi', None)
ffi.cdef("""
    typedef struct Qpick Qpick;

    Qpick* qpick_init(char*);
    void qpick_free(Qpick*);
    char* qpick_search(Qpick*, char*);

    void string_free(char*);

""")

if __name__ == '__main__':
    ffi.compile()
