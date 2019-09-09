#!/usr/bin/env bash

# Determine the current working directory
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Build a docker image from dockerfile
docker build --tag maropu-pyspark-notebook ${_DIR}

