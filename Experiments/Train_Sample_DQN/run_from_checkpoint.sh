#!/bin/sh

BASE_DIR="../../Logs/Rainbow/"
TARGET_FOLDER="20190906-153116"
LOG_PATH="$BASE_DIR$TARGET_FOLDER"



export PYTHONPATH=${PYTHONPATH}:../..
export PYTHONPATH=${PYTHONPATH}:../../agents/rainbow

python -um train \
  --base_dir=${LOG_PATH} \
  --gin_files="../../agents/rainbow/configs/hanabi_rainbow.gin"
  --gin_bindings='RainbowAgent' 
  --checkpoint_dir=${CHECKPOINT_DIR} 