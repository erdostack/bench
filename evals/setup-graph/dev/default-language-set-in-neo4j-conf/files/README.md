# trailmap

Which huts can you reach in a day, and which loops avoid the closed sections? A small planning tool for a hut-to-hut
network: huts are nodes, trail sections are relationships with a walking time and a status.

## Running it

    cp config/local.example config/local     # set GRAPH_PASSWORD
    make up                                    # Neo4j in Docker, config from conf/
    make load                                  # huts and sections from data/
    make query FILE=queries/huts_within_a_day.cypher

The app itself is a thin FastAPI layer in `trailmap/api.py`; most of the interesting work is in the saved queries.
