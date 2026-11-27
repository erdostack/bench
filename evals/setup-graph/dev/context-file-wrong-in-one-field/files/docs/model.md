# Model

    (:Lot {code, year})-[:OF_VARIETY]->(:Variety {name})
    (:Lot)-[:GROWN_FROM]->(:Lot)          // child points at parent
    (:Lot)-[:DONATED_BY]->(:Donor {name})
    (:Trial {year, outcome})-[:SOWED]->(:Lot)
    (:Trial)-[:AT]->(:Garden {name})
