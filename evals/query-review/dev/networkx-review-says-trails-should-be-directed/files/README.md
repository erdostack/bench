# trailmap

Hut finder for the national park website: which mountain huts can you reach from a trailhead within
a given distance.

    python -m unittest discover -s tests

`data/trails.json` is the trail survey export (`docs/data.md` describes it).
`trailmap.load.load_trails(path)` turns it into a graph; `trailmap.reach.huts_within(G, start, km)`
answers the question.
