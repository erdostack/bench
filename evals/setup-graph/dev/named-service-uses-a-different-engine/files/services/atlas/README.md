# atlas

Offline routing for the printed walking maps. The print pipeline runs on a machine with no network, so the
path network (junctions and path segments, exported from the council GIS) is kept in an embedded graph file,
`services/atlas/var/paths.lbug`, built by `npm run build-graph`.

    npm run build-graph -w services/atlas
    npm run lq -w services/atlas -- queries/step_free.cypher

`lq` opens the file read-only.
