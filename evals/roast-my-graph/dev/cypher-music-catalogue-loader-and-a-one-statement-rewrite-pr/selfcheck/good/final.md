Keep the current loader; his version is worse. Right now each artist and release is merged on
its unique mbid first, and link_artists only merges the CREDITED_ON relationship between the two
nodes it found. A single MERGE of the whole artist-credit-release pattern creates the entire
pattern whenever that credit is missing, even if both nodes exist, so with your uniqueness
constraints it would fail on every new credit for a known artist, and without them it would
duplicate artists and releases. The MATCH cannot skip rows here, because the upserts run first in
the same process. Details in docs/graph/ROAST.md and findings.json.
