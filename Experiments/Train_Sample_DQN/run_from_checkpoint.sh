#!/bin/sh

BASE_DIR="../../Logs/Rainbow/"
TARGET_FOLDER="20191025-183144"
LOG_PATH="$BASE_DIR$TARGET_FOLDER"



export PYTHONPATH=${PYTHONPATH}:../..
export PYTHONPATH=${PYTHONPATH}:../../agents/rainbow

python -um train \
  --base_dir=${LOG_PATH} \
  --gin_files="../../agents/rainbow/configs/hanabi_rainbow.gin"\
  --checkpoint_dir=${LOG_PATH}} 
  --gin_bindings='RainbowAgent' 
