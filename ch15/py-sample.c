#include "Python.h"
#define PYSAMPLE_MODULE
#include "py-sample.h"

static PyObject *py_gcd(PyObject *self, PyObject *args)
{
    int x, y, result;
    if (!PyArg_ParseTuple(args, "ii", &x, &y))
    {
        return NULL;
    }
    result = gcd(x, y);
    return Py_BuildValue("i", result);
}

static PyObject *py_in_mandel(PyObject *self, PyObject *args)
{
    double x0, y0;
    int n, result;
    if (!PyArg_ParseTuple(args, "ddi", &x0, &y0, &n))
    {
        return NULL;
    }
    result = in_mandel(x0, y0, n);
    return Py_BuildValue("i", result);
}

static PyObject *py_divide(PyObject *self, PyObject *args)
{
    int a, b, quotient, remainder;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
    {
        return NULL;
    }
    quotient = divide(a, b, &remainder);
    return Py_BuildValue("(ii)", quotient, remainder);
}

static PyObject *py_avg(PyObject *self, PyObject *args)
{
    PyObject *bufobj;
    Py_buffer view;
    double result;
    if (!PyArg_ParseTuple(args, "O", &bufobj))
    {
        return NULL;
    }
    if (PyObject_GetBuffer(bufobj, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }

    if (view.ndim != 1)
    {
        PyErr_SetString(PyExc_TypeError, "expected a 1-dimensional array");
        PyBuffer_Release(&view);
        return NULL;
    }

    if (strcmp(view.format, "d") != 0)
    {
        PyErr_SetString(PyExc_TypeError, "expected an array of doubles");
        PyBuffer_Release(&view);
        return NULL;
    }

    result = avg(view.buf, view.shape[0]);
    PyBuffer_Release(&view);
    return Py_BuildValue("d", result);
}

static void del_Point(PyObject *obj)
{
    printf("deleting point\n");
    free(PyCapsule_GetPointer(obj, "Point"));
}

static Point *PyPoint_AsPoint(PyObject *obj)
{
    return (Point *)PyCapsule_GetPointer(obj, "Point");
}

static PyObject *PyPoint_FromPoint(Point *p, int must_free)
{
    return PyCapsule_New(p, "Point", must_free ? del_Point : NULL);
}

static _PointAPIMethods _point_api = {
    PyPoint_AsPoint,
    PyPoint_FromPoint};

static PyObject *py_Point(PyObject *self, PyObject *args)
{
    Point *p;
    double x, y;
    if (!PyArg_ParseTuple(args, "dd", &x, &y))
    {
        return NULL;
    }
    p = (Point *)malloc(sizeof(Point));
    p->x = x;
    p->y = y;
    return PyPoint_FromPoint(p, 1);
}

static PyObject *py_distance(PyObject *self, PyObject *args)
{
    Point *p1, *p2;
    PyObject *py_p1, *py_p2;
    double result;
    if (!PyArg_ParseTuple(args, "OO", &py_p1, &py_p2))
    {
        return NULL;
    }
    if (!(p1 = PyPoint_AsPoint(py_p1)))
    {
        return NULL;
    }
    if (!(p2 = PyPoint_AsPoint(py_p2)))
    {
        return NULL;
    }
    result = distance(p1, p2);
    return Py_BuildValue("d", result);
}

static PyMethodDef SampleMethods[] = {
    {"gcd", py_gcd, METH_VARARGS, "greatest common divisor"},
    {"avg", py_avg, METH_VARARGS, "average of iterable"},
    {"in_mandel", py_in_mandel, METH_VARARGS, "mandelbrot test"},
    {"divide", py_divide, METH_VARARGS, "integer division"},
    {"Point", py_Point, METH_VARARGS, "create a point"},
    {"distance", py_distance, METH_VARARGS, "distance between points"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef samplemodule = {
    PyModuleDef_HEAD_INIT,
    "sample",
    "a sample module",
    -1,
    SampleMethods};

PyMODINIT_FUNC
PyInit_sample(void)
{
    PyObject *m;
    PyObject *py_point_api;
    m = PyModule_Create(&samplemodule);
    if (m == NULL)
        return NULL;

    py_point_api = PyCapsule_New((void *)&_point_api, "sample._point_api", NULL);
    if (py_point_api)
    {
        PyModule_AddObject(m, "_point_api", py_point_api);
    }
    return m;
}
