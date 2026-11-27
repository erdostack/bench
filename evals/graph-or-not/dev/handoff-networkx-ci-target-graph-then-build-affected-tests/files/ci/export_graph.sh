#!/bin/sh
# Writes var/graph.json from the build tool's query output.
set -eu
mkdir -p var
buildtool query --output=json-graph '//...' > var/graph.json
