# seedbank

Lineage of the varieties in a community seed bank: which lines were crossed to make which, and which
parent stocks we no longer hold.

The graph is Neo4j 2026.08.1, deployed to a local kind cluster with the chart in deploy/chart.

    make cluster up forward
    make q F=queries/lost_parents.cypher
