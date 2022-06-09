#!/usr/bin/env bash

VENVNAME=HCI_exam

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate

pip --version
pip install --upgrade pip
pip --version

# Install packages
pip install ipython
pip install jupyter
pip install matplotlib
pip install plotly


python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

deactivate
echo "build $VENVNAME"