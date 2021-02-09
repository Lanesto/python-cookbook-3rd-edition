from distutils.core import setup, Extension

setup(
    name="sample",
    ext_modules=[
        Extension(
            "sample",
            ["py-sample.c"],
            include_dirs=["/workspace/ch15"],
            define_macros=[("FOO", "1")],
            undef_macros=["BAR"],
            library_dirs=["/usr/local/lib"],
            libraries=["sample"],
        )
    ],
)

setup(
    name="ptexample",
    ext_modules=[
        Extension(
            "ptexample",
            ["pt-example.c"],
            include_dirs=[],
        )
    ],
)
