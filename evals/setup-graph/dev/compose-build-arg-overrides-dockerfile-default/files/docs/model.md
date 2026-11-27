# Model

    (:Bin {code, zone})-[:IN_AISLE]->(:Aisle {name})
    (:Bin)-[:NEXT_TO]->(:Bin)        // stored once per pair, queried in both directions

`NEXT_TO` has no distance: bins are a fixed pitch apart, so steps are counted instead.
