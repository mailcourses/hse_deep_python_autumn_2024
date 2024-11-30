import ctypes
import time

import cffi

import capi_fibs
import cyth_functions


def _fib_py_rec(n: int) -> int:
    if n < 3:
        return 1

    return _fib_py_rec(n - 1) + _fib_py_rec(n - 2)


def _fib_py_iter(n: int) -> int:
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


def run_native_python_fib(n_rec, n_iter):
    start = time.time()
    res = _fib_py_rec(n_rec)
    end = time.time()

    print(f"[python] fib rec {res=}, tt={end - start}")

    start = time.time()
    res = _fib_py_iter(n_iter)
    end = time.time()

    print(f"[python] fib iter {res=}, tt={end - start}")


def run_ctypes_fib(n_rec, n_iter):
    dll = ctypes.CDLL("./ctypes_utils/libfunctions.so")

    dll.fib_rec.argtypes = [ctypes.c_int]
    dll.fib_rec.restype = ctypes.c_int

    dll.fib_iter.argtypes = [ctypes.c_int]
    dll.fib_iter.restype = ctypes.c_int

    start = time.time()
    res = dll.fib_rec(ctypes.c_int(n_rec))
    end = time.time()
    print(f"[ctypes] fib rec {res=}, tt={end - start}")

    start = time.time()
    res = dll.fib_iter(n_iter)
    end = time.time()
    print(f"[ctypes] fib iter {res=}, tt={end - start}")


def run_cffi_fib(n_rec, n_iter):
    ffi = cffi.FFI()
    lib = ffi.dlopen("./ctypes_utils/libfunctions.so")

    ffi.cdef(
        "int fib_rec(int n);\n"
        "int fib_iter(int n);\n"
    )

    start = time.time()
    res = lib.fib_rec(n_rec)
    end = time.time()
    print(f"[cffi] fib rec {res=}, tt={end - start}")

    start = time.time()
    res = lib.fib_iter(n_iter)
    end = time.time()
    print(f"[cffi] fib iter {res=}, tt={end - start}")


def run_capi_fib(n_rec, n_iter):
    start = time.time()
    res = capi_fibs.fib_rec_api(n_rec)
    end = time.time()
    print(f"[capi] fib rec {res=}, tt={end - start}")

    start = time.time()
    res = capi_fibs.fib_iter_api(n_iter)
    end = time.time()
    print(f"[capi] fib iter {res=}, tt={end - start}")


def run_cyth_fib(n_rec, n_iter):
    start = time.time()
    res = cyth_functions.fib_cy_rec(n_rec)
    end = time.time()
    print(f"[cython] fib rec {res=}, tt={end - start}")

    start = time.time()
    res = cyth_functions.fib_cy_iter(n_iter)
    end = time.time()
    print(f"[cython] fib iter {res=}, tt={end - start}")


def run():
    n_rec, n_iter = 36, 40

    run_native_python_fib(n_rec, n_iter)
    print("--------\n")

    run_ctypes_fib(n_rec, n_iter)
    print("--------\n")

    run_cffi_fib(n_rec, n_iter)
    print("--------\n")

    run_capi_fib(n_rec, n_iter)
    print("--------\n")

    run_cyth_fib(n_rec, n_iter)
    print("--------\n")


if __name__ == "__main__":
    run()


