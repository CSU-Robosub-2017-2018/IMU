#!/bin/bash


echo "Start doxygen"

cd doc/html
rm -r -f *
cd ..
doxygen config.dox
cd html
firefox index.html
