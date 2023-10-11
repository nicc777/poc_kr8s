#!/bin/sh

python3 -m venv venv
. venv/bin/activate

# pip3 install --user virtualenv
pip3 install --upgrade setuptools 
pip3 install --upgrade build

pip3 install dist/*.tar.gz

