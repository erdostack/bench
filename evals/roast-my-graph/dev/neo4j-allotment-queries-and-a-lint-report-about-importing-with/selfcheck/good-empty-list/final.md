Nothing to change now. The four "deprecated" queries are written correctly for Neo4j 5.15, which is
what you run until March 2027. The scope-clause form CALL (p) { } is a 5.23 addition, so following the
lint would break production. Rewrite when you upgrade.
