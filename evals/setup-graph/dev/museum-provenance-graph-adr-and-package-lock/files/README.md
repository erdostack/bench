# provenance

Ownership history of the museum's collection: objects, owners, dealers and the transfers between them,
for the provenance researchers. The graph is an embedded LadybugDB database (`var/provenance.lbdb`,
opened in process by `@ladybugdb/core`; there is no server).

    npm ci
    npm run load                         # rebuild var/ from data/*.csv
    npm run q -- queries/chain.cypher OBJ-0031

Architecture decisions are in docs/adr/.
