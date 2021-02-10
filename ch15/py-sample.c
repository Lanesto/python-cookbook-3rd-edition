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
    PySys_WriteStdout("deleting point\n");
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

void print_chars(char *s)
{
    while (*s)
    {
        PySys_WriteStdout("%2x ", (unsigned char)*s);
        s++;
    }
    PySys_WriteStdout("\n");
}

static PyObject *py_print_chars(PyObject *self, PyObject *args)
{
    char *s;
    if (!PyArg_ParseTuple(args, "s", &s))
    {
        return NULL;
    }
    print_chars(s);
    Py_RETURN_NONE;
}

void print_wchars(wchar_t *s, int len)
{
    int n = 0;
    while (n < len)
    {
        PySys_WriteStdout("%x ", s[n]);
        n++;
    }
    PySys_WriteStdout("\n");
}

static PyObject *py_print_wchars(PyObject *self, PyObject *args)
{
    wchar_t *s;
    Py_ssize_t len;
    if (!PyArg_ParseTuple(args, "u#", &s, &len))
    {
        return NULL;
    }
    print_wchars(s, len);
    Py_RETURN_NONE;
}

static PyObject *py_get_filename(PyObject *self, PyObject *args)
{
    PyObject *bytes;
    char *filename;
    Py_ssize_t len;
    if (!PyArg_ParseTuple(args, "O&", PyUnicode_FSConverter, &bytes))
    {
        return NULL;
    }
    PyBytes_AsStringAndSize(bytes, &filename, &len);
    PySys_WriteStdout(filename);
    Py_DECREF(bytes);
    Py_RETURN_NONE;
}

#define CHUNK_SIZE 8192

static PyObject *py_consume_file(PyObject *self, PyObject *args)
{
    PyObject *obj;
    PyObject *read_meth;
    PyObject *result = NULL;
    PyObject *read_args;
    if (!PyArg_ParseTuple(args, "O", &obj))
    {
        return NULL;
    }
    if ((read_meth = PyObject_GetAttrString(obj, "read")) == NULL)
    {
        return NULL;
    }
    read_args = Py_BuildValue("(i)", CHUNK_SIZE);
    while (1)
    {
        PyObject *data;
        PyObject *enc_data;
        char *buf;
        Py_ssize_t len;
        if ((data = PyObject_Call(read_meth, read_args, NULL)) == NULL)
        {
            goto final;
        }
        if (PySequence_Length(data) == 0)
        {
            Py_DECREF(data);
            break;
        }
        if ((enc_data = PyUnicode_AsEncodedString(data, "utf-8", "strict")) == NULL)
        {
            Py_DECREF(data);
            goto final;
        }
        PyBytes_AsStringAndSize(enc_data, &buf, &len);
        PySys_WriteStdout(buf);
        // write(1, buf, len);
        Py_DECREF(enc_data);
        Py_DECREF(data);
    }
    result = Py_BuildValue("");
final:
    Py_DECREF(read_meth);
    Py_DECREF(read_args);
    return result;
}

static PyObject *py_consume_iterable(PyObject *self, PyObject *args)
{
    PyObject *obj;
    PyObject *iter;
    PyObject *item;
    if (!PyArg_ParseTuple(args, "O", &obj))
    {
        return NULL;
    }
    if ((iter = PyObject_GetIter(obj)) == NULL)
    {
        return NULL;
    }
    while ((item = PyIter_Next(iter)) != NULL)
    {
        PySys_WriteStdout("got item\n");
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return Py_BuildValue("");
}

static PyMethodDef SampleMethods[] = {
    {"gcd", py_gcd, METH_VARARGS, "greatest common divisor"},
    {"avg", py_avg, METH_VARARGS, "average of iterable"},
    {"in_mandel", py_in_mandel, METH_VARARGS, "mandelbrot test"},
    {"divide", py_divide, METH_VARARGS, "integer division"},
    {"Point", py_Point, METH_VARARGS, "create a point"},
    {"distance", py_distance, METH_VARARGS, "distance between points"},
    {"print_chars", py_print_chars, METH_VARARGS, "print each characters"},
    {"print_wchars", py_print_wchars, METH_VARARGS, "print each characters"},
    {"get_filename", py_get_filename, METH_VARARGS, "print python filename from C"},
    {"consume_file", py_consume_file, METH_VARARGS, "consume file-like object"},
    {"consume_iterable", py_consume_iterable, METH_VARARGS, "consume iterable"},
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
