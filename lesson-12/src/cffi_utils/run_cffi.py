import cffi
from functools import reduce


def run():
    ffi = cffi.FFI()
    lib = ffi.dlopen("../ctypes_utils/libfunctions.so")

    ffi.cdef(
        "int sum(int* arr, int n);\n"
        "int fib_rec(int n);\n"
    )

    lst = list(range(10, 20))
    len_lst = len(lst)

    arr = ffi.new("int[]", lst)
    print(f"{type(arr)=}")

    res = lib.sum(arr, len_lst)
    print(f"{res=}, {sum(lst)=}")

    res = lib.fib_rec(36)
    print(f"fib {res=}")


def run_builder():
    builder = cffi.FFI()
    builder.cdef("int mult(int* arr, int len);")

    builder.set_source(
        "tmp_cffi_utils",
        """
        int mult(int* arr, int len)
        {
            int res = 1;
            for (int i = 0; i < len; ++i)
            {
                res *= arr[i];
            }
            return res;
        }
        """
    )
    builder.compile()


    from tmp_cffi_utils import lib

    print(f"{dir(lib)=}")

    lst = list(range(10, 15))
    len_lst = len(lst)

    arr = builder.new("int[]", lst)
    print(f"{type(arr)=}")

    res = lib.mult(arr, len_lst)

    print(f"{res=}, {reduce(lambda x, y: x * y, lst)=}")


if __name__ == "__main__":
    run()
    run_builder()
