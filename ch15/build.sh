#!/bin/bash

if [ ! -a "/usr/local/lib/libsample.so" ]; then
    cp libsample.so /usr/local/lib/
fi

# --rpath option to temporarily fix error locating library file
python setup.py build_ext --inplace --rpath=/usr/local/lib
