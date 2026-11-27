Decision: graph-database

Ravi has a point. 1.9M redirects with chains and 214 loops is exactly the kind of data a graph database models
natively: chains are paths, loops are cycles, and Neo4j can find both with one pattern. Load the table nightly and
let the job query the end of each path.
