#!/bin/bash
cd ./docs

rm -Rf ./_build

make html

cd ../