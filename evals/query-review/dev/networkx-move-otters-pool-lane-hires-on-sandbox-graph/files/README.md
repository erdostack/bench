# lanegraph

Lane allocation for Brackwater's public pools, as NetworkX graphs saved as GraphML: pools, lanes, clubs and
their lane hires.

- `graphs/published.graphml`: the allocation the booking system and the poolside screens load.
- `graphs/sandbox.graphml`: the sandbox. See `docs/graphs.md`.
- `bin/lane <graph> <script.py>`: load `graphs/<graph>.graphml`, call the script's `run(G)`, save it back.
- `scripts/reset_sandbox.py`: copy the published graph over the sandbox.
- `docs/graphs.md`, `docs/model.md`.
