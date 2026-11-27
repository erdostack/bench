# seedline

Pedigree of the seed bank's accessions: which accession was bred, selected or regenerated from which one.
Curators ask for every ancestor of a line and for the lines that share a parent.

Two Go modules live here: `pedigree/` (the query tool) and `tools/importer/` (loads the curation exports).
Both use embedded Kuzu 0.10.0 through github.com/kuzudb/go-kuzu (see pedigree/go.mod); the database is the
directory `data/pedigree.kz`, and there is no server.

    make q F=queries/ancestors.cypher ID=ACC-00412

The query tool opens the database read-only. `make import` rebuilds it from `data/exports/` and is run by
the curation team after each regeneration cycle.
