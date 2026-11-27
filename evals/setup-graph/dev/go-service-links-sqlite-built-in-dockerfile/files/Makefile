IMAGE ?= stopgraph:dev
Q ?= queries/reachable_within.sql
ARGS ?=

.PHONY: image q

image:
	docker build -t $(IMAGE) .

q:
	docker run --rm -v $(CURDIR):/work $(IMAGE) stopq -db data/stops.db -f $(Q) $(ARGS)
