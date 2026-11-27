# Deploying the graph

Create the auth secret once per cluster:

    kubectl create secret generic pantry-graph-auth --from-literal=NEO4J_AUTH=neo4j/<choose-one>

The chart's defaults (`deploy/chart/values.yaml`) are what staging uses. Local overrides live in
`deploy/values-local.yaml`.
