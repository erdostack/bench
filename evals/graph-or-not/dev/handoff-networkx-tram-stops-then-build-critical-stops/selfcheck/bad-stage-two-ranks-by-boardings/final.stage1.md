Decision: in-process-library. Written up in docs/graph/DECISION.md.

"Critical" as ops define it is a stop whose closure splits the network: a cut vertex (articulation point). That is a
whole-graph property, computed in one pass over the graph, and at 3,100 stops and 3,900 links the whole network fits
in a few megabytes. networkx (already in requirements.txt) does it with `articulation_points` in well under a second,
inside the nightly report job and its 40 minute window. A graph database would add a server for three analysts with
nobody to run it, to answer a question the library answers in-process. Recursive SQL walks from a start stop; it is
the wrong shape for "which single closure disconnects anything".
