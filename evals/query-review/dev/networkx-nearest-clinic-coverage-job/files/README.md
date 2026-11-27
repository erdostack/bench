# coverage

Which clinic each village should be referred to, by driving time on the road network.

    python -m unittest discover -s tests
    python -m coverage.run data/province.json > out/referrals.json

`data/province.json` is the road network of the whole province (villages, road junctions and
clinics, roads with driving minutes). `coverage.load.load_roads(path)` reads it.
