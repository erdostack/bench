# depot-network

The current shape of our distribution network in Neo4j 5.26: depots, what they stock, who is based where, and
which depots are near each other (about 300 depots, 40,000 SKUs). It is a picture of *now*: shipments, stock movements and staff history live
in the WMS and HR systems, which are the record. Nothing in this graph is history.

## Relationships

- `(:Depot)-[:STOCKS {qty}]->(:Sku)`
- `(:Staff)-[:BASED_AT {since}]->(:Depot)`
- `(:Depot)-[:IN_REGION]->(:Region)`
- `(:Depot)-[:NEAR {km}]->(:Depot)`: recomputed every night by `jobs/near.py` from depot coordinates

## Closing a depot

`graph/closure.cypher`, run in order with `$closing` and `$target` depot codes, inside one transaction by
`tools/close_depot.py`. Stock and staff move to the target depot, then the closed depot is removed.
