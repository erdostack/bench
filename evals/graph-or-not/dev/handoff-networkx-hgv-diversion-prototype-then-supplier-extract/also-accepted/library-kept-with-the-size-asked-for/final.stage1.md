Decision: in-process-library

Keep the prototype's networkx for now, but this is provisional: I don't know whether it fits until we have the
extract's segment count. The worker's hard limit is 1.5 GB and the 38,000-segment sample takes about 70 MB, so
anything up to about 15 times the sample fits; the 4 million-segment national product would not. Can you send
the segment count as soon as the supplier gives it? Then we confirm or move. No graph database before that.
Recorded in docs/adr/0002-diversion-network.md.
