#include <Python.h>

double call_func(PyObject *func, double x, double y)
{
    PyObject *args;
    PyObject *kwargs;
    PyObject *result = 0;
    double retval;
    PyGILState_STATE state = PyGILState_Ensure();
    if (!PyCallable_Check(func))
    {
        fprintf(stderr, "call_func: expected a callable\n");
        goto fail;
    }
    args = Py_BuildValue("(dd)", x, y);
    kwargs = NULL;
    result = PyObject_Call(func, args, kwargs);
    Py_DECREF(args);
    Py_XDECREF(kwargs);
    if (PyErr_Occurred())
    {
        PyErr_Print();
        goto fail;
    }
    if (!PyFloat_Check(result))
    {
        fprintf(stderr, "call_func: callable didn't return a float\n");
        goto fail;
    }
    retval = PyFloat_AsDouble(result);
    Py_DECREF(result);
    PyGILState_Release(state);
    return retval;

fail:
    Py_XDECREF(result);
    PyGILState_Release(state);
    abort();
}

int main()
{
    PyObject *pow_func;
    double x;

    Py_Initialize();
    pow_func = import_name("math", "pow");
    for (x = 0.0; x < 10.0; x += 0.1)
    {
        printf("%0.2f %0.2f\n", x, call_func(pow_func, x, 2.0));
    }

    Py_DECREF(pow_func);
    Py_Finalize();
    return 0;
}