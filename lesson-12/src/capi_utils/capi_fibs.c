#include <stdlib.h>
#include <stdio.h>
#include <Python.h>


int fib_rec(int n)
{
    if (n < 3)
        return 1;

    return fib_rec(n - 1) + fib_rec(n - 2);
}


PyObject* capi_fibs_fib_rec_api(PyObject* self, PyObject* args)
{
    int n = 0;
    if (!PyArg_ParseTuple(args, "i", &n))
    {
        printf("Failed to parse args");
        return NULL;
    }

    int res = fib_rec(n);

    return PyLong_FromLong(res);
}


PyObject* capi_fibs_fib_iter_api(PyObject* self, PyObject* args)
{
    int n = 0;
    if (!PyArg_ParseTuple(args, "i", &n))
    {
        printf("Failed to parse args");
        return NULL;
    }

    int a = 0, b = 1;
    for (int i = 0; i < n; ++i)
    {
        int tmp = b;
        b = a + b;
        a = tmp;
    }

    return Py_BuildValue("i", a);
}


static PyMethodDef fibs[] = {
    {"fib_rec_api", capi_fibs_fib_rec_api, METH_VARARGS, "recur fib with capi"},
    {"fib_iter_api", capi_fibs_fib_iter_api, METH_VARARGS, "iter fib with capi"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_capi_fibs = {
    PyModuleDef_HEAD_INIT, "capi_fibs", NULL, -1, fibs
};


PyMODINIT_FUNC PyInit_capi_fibs()
{
    return PyModule_Create( &module_capi_fibs );
}

