int sum(int* arr, int len)
{
    int res = 0;
    for (int i = 0; i < len; i += 1)
    {
        res += arr[i];
    }
    return res;
}


int fib_rec(int n)
{
    if (n < 3)
        return 1;

    return fib_rec(n - 1) + fib_rec(n - 2);
}


int fib_iter(int n)
{
    int a = 0, b = 1;
    for (int i = 0; i < n; ++i)
    {
        int tmp = b;
        b = a + b;
        a = tmp;
    }
    return a;
}
