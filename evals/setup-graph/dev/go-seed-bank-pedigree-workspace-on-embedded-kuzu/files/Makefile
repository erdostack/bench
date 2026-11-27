F ?= queries/ancestors.cypher
ID ?= ACC-00412

.PHONY: q import

q:
	cd pedigree && go run ./cmd/lineage -db ../data/pedigree.kz -f ../$(F) id=$(ID)

import:
	cd tools/importer && go run . -db ../../data/pedigree.kz -in ../../data/exports
