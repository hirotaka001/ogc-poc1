#!/bin/bash

cd $(dirname $0)

python ./setup.py bdist_wheel
