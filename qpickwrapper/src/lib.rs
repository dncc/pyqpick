#![crate_type = "dylib"]

extern crate libc;
extern crate qpick;

use std::ffi::{CStr, CString};

/// Get an immutable reference from a raw pointer
macro_rules! ref_from_ptr {
    ($p:ident) => (unsafe {
        assert!(!$p.is_null());
        &*$p
    })
}

/// Get the object referenced by the raw pointer
macro_rules! val_from_ptr {
    ($p:ident) => (unsafe {
        assert!(!$p.is_null());
        Box::from_raw($p)
    })
}

/// Declare a function that frees a struct's memory
macro_rules! make_free_fn {
    ($name:ident, $t:ty) => (
    #[no_mangle]
    pub extern fn $name(ptr: $t) {
        assert!(!ptr.is_null());
        val_from_ptr!(ptr);
    })
}

pub fn str_to_cstr(string: &str) -> *mut libc::c_char {
    CString::new(string).unwrap().into_raw()
}

pub fn cstr_to_str<'a>(s: *mut libc::c_char) -> &'a str {
    let cstr = unsafe { CStr::from_ptr(s) };
    cstr.to_str().unwrap()
}

pub fn to_raw_ptr<T>(v: T) -> *mut T {
    Box::into_raw(Box::new(v))
}

use qpick::Qpick;

// `#[no_mangle]` warns for lifetime parameters,
// a known issue: https://github.com/rust-lang/rust/issues/40342
#[no_mangle]
pub extern "C" fn qpick_init(path: *mut libc::c_char) -> *mut Qpick {
    let path = cstr_to_str(path);
    let qpick = Qpick::from_path(path.to_string());
    to_raw_ptr(qpick)
}
make_free_fn!(qpick_free, *mut Qpick);

#[no_mangle]
pub extern "C" fn string_free(s: *mut libc::c_char) {
    unsafe { CString::from_raw(s) };
}

#[no_mangle]
pub extern "C" fn qpick_search(ptr: *mut Qpick, query: *mut libc::c_char) -> *const libc::c_char {
    let query = cstr_to_str(query);
    let s = ref_from_ptr!(ptr).search(query);
    CString::new(s).unwrap().into_raw()
}
