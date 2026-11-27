# playlist-sim

Nightly job that builds the "similar playlists" graph (NetworkX, undirected, edge attribute `weight`
in (0, 1]) from co-listening and saves it for the shelf service. `recs/nightly.py` is the job;
`data/similar_playlists.json` is last night's graph in node-link format. What the shelf shows is in
`docs/shelf.md`.
