#!/usr/bin/env bash

# get present working dirname
current_dir=$(pwd)
echo "current_dir":"$current_dir"

# get script_dir
script_dir=$(dirname $0)
if [ $script_dir = '.' ]
then
  script_dir="$current_dir"
fi
#echo "script_dir":"$script_dir"

# get project_dir
project_dir="$(dirname "$script_dir")"
#echo "project_dir":"$project_dir"

# create LOG_DIR & MODEL_DIR path
LOGS_DIR="${project_dir}/logs/"
echo "LOG_DIR":$LOGS_DIR

MODELS_DIR=${project_dir}"/model/"
echo "MODEL_DIR":$MODELS_DIR
echo '-------------------'

# Create logs folder if doesn't exist
if '[' ! -d "$LOGS_DIR" ']'
then
  echo "Creating new log directory"
  mkdir $LOGS_DIR
else
  echo "Appending logs with existing log files"
fi
echo '-------------------'


# get the latest model from MODEL_DIR
LATEST_MODEL_DIR=$(find ${MODELS_DIR}* -type d -prune | tail -n 1)
echo "LATEST_MODEL_DIR":$LATEST_MODEL_DIR


echo '-------------------'
# start process with LATEST_MODEL
#start p1
echo "started p1 with pid: "
nohup python p1.py & echo $!


#start p2
echo "started p2 with pid: "
nohup python p2.py & echo $!
