#!/bin/bash
set -euxo pipefail

# Check that we are running from the right directory.
if [ ! "${PWD##*/}" = "visual_relation" ]; then
    echo "Script must be run from visual_relation directory" >&2
    exit 1
fi

DIRS=("glove" "VRD/sg_dataset/samples")

RELOAD=false
# Check if at least any file is missing. If so, reload all data.
for directory_name in "${DIRS[@]}"
do
    if [ ! -d "data/$directory_name" ]; then
        RELOAD=true
    fi
done

ANNOTATIONS_URL="https://www.dropbox.com/s/bnfhm6kt9xumik8/vrd.zip"
SAMPLE_IMAGES_URL="https://github.com/Prof-Lu-Cewu/Visual-Relationship-Detection.git"
GLOVE_URL="http://nlp.stanford.edu/data/wordvecs/glove.6B.zip"

if [ "$RELOAD" = true ]; then
    if [ -d "data" ]; then rm -Rf "data"; fi
    mkdir -p data
    cd data

    # download and unzip metadata and annotations
    wget $ANNOTATIONS_URL
    unzip vrd.zip

    # Delete the zip files.
    rm vrd.zip
    cd VRD

    # Download and unzip sample images
    mkdir sg_dataset
    cd sg_dataset
    git clone $SAMPLE_IMAGES_URL
    mv Visual-Relationship-Detection/samples ./
    rm -r Visual-Relationship-Detection
    cd ../..

    mkdir -p glove
    cd glove

    wget $GLOVE_URL
    unzip glove.6B.zip

    # Delete the zip files
    rm  glove.6B.zip
    cd ../..
fi
