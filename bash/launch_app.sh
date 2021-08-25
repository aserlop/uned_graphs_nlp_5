#!/usr/bin/env bash

ENV_NAME="uned_graphs_nlp_5"

TASK_PATH='../python/textrank/task.py'
JSON_PATH='../resources/app_textrank.json'

source activate $ENV_NAME
python $TASK_PATH $JSON_PATH
conda deactivate