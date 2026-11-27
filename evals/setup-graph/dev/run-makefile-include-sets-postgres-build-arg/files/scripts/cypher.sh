#!/bin/sh
# Run one openCypher file against the huts graph through AGE's cypher() function, read-only.
set -eu
body=$(cat "$1")
docker exec -i hutlink-db psql -U postgres -v ON_ERROR_STOP=1 <<SQL
LOAD 'age';
SET search_path = ag_catalog, "\$user", public;
SET default_transaction_read_only = on;
SELECT * FROM cypher('huts', \$\$ $body \$\$) AS (result agtype);
SQL
