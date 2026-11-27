Decision: recursive-sql. Recorded in docs/adr/0003-circuit-trace.md.

The trace is slow because it makes a round trip per pin: about 600 queries and 2.1 s on the biggest of the 28
variants (9,400 pins and splices, 14,000 wires). Loaded into networkx the same variant is 45 MB, loads in 90 ms and
traces in 0.4 ms, and it only changes at the monthly engineering release, so the viewer can hold it in each of its
512 MB containers. A graph database would be a server and a monthly load for something that already takes under a
millisecond.
