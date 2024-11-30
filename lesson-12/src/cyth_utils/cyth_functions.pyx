cpdef fib_cy_rec(int n):
    if n < 3:
        return 1

    return fib_cy_rec(n - 1) + fib_cy_rec(n - 2)


cpdef fib_cy_iter(int n):
    cdef int a = 0
    cdef int b = 1

    for _ in range(n):
        a, b = b, a + b

    return a
