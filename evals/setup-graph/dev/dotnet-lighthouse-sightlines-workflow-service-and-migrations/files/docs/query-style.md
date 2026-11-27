# Query style

- Cypher 5. Nothing from the newer Cypher 25 dialect, so the files run on the server as it is set up.
- One query per file in queries/, a comment line on top.
- Parameters, never string concatenation.
- SEES is stored once per pair, from the lower code to the higher; match it undirected.
