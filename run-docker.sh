#!/usr/bin/env bash

# Determine the current working directory
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the custom docker image
docker run --rm -p 8888:8888 -p 5000:5000 --user root --name pyspark-notebook -v ${_DIR}:/home/jovyan \
  -e JUPYTER_ENABLE_LAB=yes maropu-pyspark-notebook

