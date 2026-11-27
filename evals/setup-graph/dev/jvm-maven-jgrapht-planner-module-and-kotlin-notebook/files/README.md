# hutnet

Plans multi-day hut-to-hut tours. There is no database: `planner/` loads the hut list and the trail
segments from `data/` into an in-memory graph (JGraphT 1.4.0) and answers route questions with
Dijkstra and Yen's k-shortest paths.

## Running

    bin/route H07 H09          # quickest route between two huts
    bin/route H07 H09 3        # the three quickest alternatives

Builds with the Maven wrapper; Java 21 (see `.sdkmanrc`).

## Data

`data/huts.csv` and `data/trails.csv` are hand-maintained. A trail is one-way when the walking time
differs by direction; add both rows if it does not.

`notebooks/explore.ipynb` is the scratch notebook from the first season (Kotlin kernel).
