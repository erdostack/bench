#!/bin/sh
# Run one saved query against the stemma database.
set -eu
exec sqlite3 -readonly -header -column data/stemma.db < "$1"
