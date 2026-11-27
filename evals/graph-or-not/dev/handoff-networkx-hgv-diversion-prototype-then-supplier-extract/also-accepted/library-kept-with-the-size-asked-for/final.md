Decision: in-process-library

The open question was the extract's size against the worker's hard 1.5 GB limit. The county sample was 38,000
segments in about 70 MB; 180,000 segments is about 4.7 times that, so roughly 330 MB, comfortably inside 1.5 GB.
Routes took 30 ms on the sample and the budget is 2 s at about 300 checks a day, so time is no concern either.
Keep networkx in the worker; no graph database. docs/adr/0002-diversion-network.md is updated.
