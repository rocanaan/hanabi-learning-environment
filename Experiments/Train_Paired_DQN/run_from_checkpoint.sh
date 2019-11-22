#!/bin/sh

BASE_DIR="../../Logs/Paired/"
TARGET_FOLDER="Internal5500"
CUR_DATE=`date "+%Y%m%d-%H%M%S"`
LOG_PATH="$BASE_DIR$TARGET_FOLDER"
NEW_LOG_PATH="$BASE_DIR$TARGET_FOLDER/$CUR_DATE"





export PYTHONPATH=${PYTHONPATH}:../..
export PYTHONPATH=${PYTHONPATH}:../../agents/rainbow
export PYTHONPATH=${PYTHONPATH}:../../Experiments/Rulebased
# export PYTHONPATH=${PYTHONPATH}:/home/jupyter/Notebooks/Rodrigo/hanabilearningenvironment/
# export PYTHONPATH=${PYTHONPATH}:/home/jupyter/Notebooks/Rodrigo/hanabilearningenvironment/Experiments/Rulebased
# export PYTHONPATH=${PYTHONPATH}:/home/jupyter/Notebooks/Rodrigo/hanabilearningenvironment/agents/rainbow
# export CUDA_VISIBLE_DEVICES=""



python3 -um train_paired \
  --base_dir=${LOG_PATH} \
  --gin_files="hanabi_rainbow.gin"\
  --checkpoint_dir=${LOG_PATH} \
  --checkpoint_version=5500