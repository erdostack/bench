# Model

    (:Tree {tag, planted})-[:OF_VARIETY]->(:Variety {name})
    (:Tree)-[:SCION_FROM]->(:Tree)          // grafted tree points at the tree the scion wood came from
    (:Tree)-[:ON_ROOTSTOCK]->(:Rootstock {name})
    (:Tree)-[:IN_ROW]->(:Row {name})-[:ADJACENT_TO]->(:Row)
    (:Variety)-[:POLLINATED_BY]->(:Variety)
