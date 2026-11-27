# pantry

Ingredient substitutions for a recipe site: what can stand in for what, under which diet, and how many
swaps a recipe needs before it becomes vegan. The graph is embedded Neo4j 2026.02.2, opened in-process
from `build/graph-db`; there is no server.

    ./gradlew seed                                   # build the store from data/
    ./gradlew runCypher -Pfile=queries/vegan_swaps.cypher
