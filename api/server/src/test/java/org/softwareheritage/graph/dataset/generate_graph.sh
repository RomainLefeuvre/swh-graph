#!/bin/bash

# Build Docker work environment
toplevel_dir=`git rev-parse --show-toplevel`
mkdir -p dockerfiles
cp $toplevel_dir/compression/{compress_graph.sh,Dockerfile} dockerfiles/
docker build --tag swh-graph-test dockerfiles

# Setup input for compression script
tr ' ' '\n' < graph.edges.csv | sort -u > graph.nodes.csv
gzip --force --keep graph.edges.csv
gzip --force --keep graph.nodes.csv

docker run                                          \
    --name swh-graph-test --rm --tty --interactive  \
    --volume $(pwd):/data swh-graph-test:latest     \
    ./compress_graph.sh /data/graph /data/