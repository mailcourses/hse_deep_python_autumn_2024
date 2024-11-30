import ctypes


def run():
    dll = ctypes.CDLL("./libfunctions.so")
    dll.sum.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)

    lst = list(range(10, 20))
    lst_len = len(lst)

    arrtype = ctypes.c_int * lst_len
    res = dll.sum(arrtype(*lst), ctypes.c_int(lst_len))
    print(f"{res=}, {sum(lst)=}")


def run_libc():
    # dll = ctypes.CDLL(None)
    dll = ctypes.CDLL("/usr/lib/libstdc++.6.dylib")
    dll.strstr.argtype = (ctypes.c_char_p, ctypes.c_char_p)
    dll.strstr.restype = ctypes.c_char_p

    print(f'{dll.strstr(b"ababac", b"ba")=}')
    print(f'{dll.strstr(b"ababac", b"qwer")=}')
    print(f'{dll.strstr(b"ababac", b"bac")=}')


if __name__ == "__main__":
    run()
    run_libc()
