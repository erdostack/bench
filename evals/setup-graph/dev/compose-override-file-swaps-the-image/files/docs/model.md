# Model

    (:Species {name, trophic_level})-[:EATS]->(:Species)
    (:Species)-[:LIVES_IN]->(:Zone {name})

`EATS` points from the eater to the eaten. Trophic level is stored, not derived, because the course hands it out
as a given.
