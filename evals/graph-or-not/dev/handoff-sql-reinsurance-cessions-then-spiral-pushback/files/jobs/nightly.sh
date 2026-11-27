#!/bin/sh
set -eu
psql "$TREATY_DSN" -v ON_ERROR_STOP=1 -f exposure/rollup.sql --csv > out/exposure.csv
