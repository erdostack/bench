# Model

    (:Sailing {id, departs, arrives})-[:DEPARTS_FROM]->(:Port {code, name})
    (:Sailing)-[:ARRIVES_AT]->(:Port)

A sailing is a node, not a relationship, because the planner needs to chain "arrive, wait, depart" and compare
times on consecutive sailings.
