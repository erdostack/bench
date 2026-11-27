# thesaurus

A controlled vocabulary for a regional archive: preferred terms, broader/narrower links and
"use for" cross-references. The data is in an embedded Neo4j 5.26 LTS store under `var/thesaurus`;
there is no database server to run.

    ./mvnw -q package
    bin/cypher queries/orphan_terms.cypher

Model: `(:Term {label, scheme})`, `(:Term)-[:BROADER]->(:Term)`, `(:Term)-[:USE_FOR]->(:Alias)`.
