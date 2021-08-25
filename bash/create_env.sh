#!/usr/bin/env bash

ENV_NAME="uned_graphs_nlp_5"
KERNEL_NAME="k_uned_graphs_nlp_5"

conda create -n $ENV_NAME python=3.7

pushd .
cd ../python
source activate $ENV_NAME
python setup.py clean
pip install .
python -m ipykernel install --user --name $ENV_NAME --display-name $KERNEL_NAME
conda deactivate
popd
