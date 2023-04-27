#!/bin/bash

# config script
BASE_PATH="/usr/bin/python"
PYTHON_PATH="$BASE_PATH$1"
VENV_PATH="venvs/$1"
[ ! -f "$PYTHON_PATH" ] && echo "Directory $PYTHON_PATH DOES NOT exists." && exit

echo "Testing with python version '$1'"

# generate new venv
rm -r "$VENV_PATH" &> /dev/null
virtualenv  --python="$PYTHON_PATH" "$VENV_PATH"
source "$VENV_PATH/bin/activate"  &> /dev/null \
|| source "$VENV_PATH/local/bin/activate"  &> /dev/null \
|| (echo "Error"; exit)

# install module and his dependencies
python -m pip install --upgrade pip || (echo "Error update pip"; exit)
pip install -e .[dev,test] || (echo "Error install module"; exit)


# execute module's tests
pytest || (echo "Error pytest"; exit)

# build and publish module
rm -r dist &> /dev/null
python -m build || (echo "Error build"; exit)
#twine upload dist/* -r pypitest || (echo "Error twine"; exit)

source deactivate
