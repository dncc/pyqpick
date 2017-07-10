from cffi import FFI

ffi = FFI()
ffi.set_source('rust_qpick._ffi', None)
ffi.cdef("""
    typedef struct Qpick Qpick;

    Qpick* qpick_init(char*);
    void qpick_free(Qpick*);
    char* qpick_get_as_string(Qpick*, char*);
    void string_free(char*);

    /**
       Iterator
    **/
    typedef struct {
        uint64_t  qid;
        float     sc;
    } QpickItem;

    typedef struct QpickResults QpickResults;

    QpickResults* qpick_get(Qpick*, char*, uint32_t);
    QpickItem* qpick_iter_next(QpickResults*);

    void qpick_results_free(QpickResults*);
    void qpick_item_free(QpickItem*);


""")

if __name__ == '__main__':
    ffi.compile()
