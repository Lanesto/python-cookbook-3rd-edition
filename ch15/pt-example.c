#include "py-sample.h"

static PyObject *print_point(PyObject *self, PyObject *args)
{
    PyObject *obj;
    Point *p;
    if (!PyArg_ParseTuple(args, "O", &obj))
    {
        return NULL;
    }
    p = PyPoint_AsPoint(obj);
    if (!p)
    {
        return NULL;
    }
    printf("%f %f\n", p->x, p->y);
    return Py_BuildValue("");
}

static PyMethodDef PtExampleMethods[] = {
    {"print_point", print_point, METH_VARARGS, "output a point"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef ptexamplemodule = {
    PyModuleDef_HEAD_INIT,
    "ptexample",
    "a module that imports an api",
    -1,
    PtExampleMethods};

PyMODINIT_FUNC
PyInit_ptexample(void)
{
    PyObject *m;
    m = PyModule_Create(&ptexamplemodule);
    if (m == NULL)
        return NULL;

    if (!import_sample())
    {
        return NULL;
    }
    return m;
}