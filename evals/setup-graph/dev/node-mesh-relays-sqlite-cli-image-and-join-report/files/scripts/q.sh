#!/bin/sh
# npm run q -- <file.sql>: run one query read-only through the meshwatch-sqlite image
set -eu
[ $# -eq 1 ] || { echo "usage: npm run q -- <file.sql>" >&2; exit 2; }
exec docker run --rm -i -v "$PWD:/work:ro" meshwatch-sqlite -readonly -header -column data/mesh.db < "$1"
