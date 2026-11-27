Q ?= queries/basket_bridges.cypher

.PHONY: snapshot query

snapshot:
	python -m lab.snapshot exports/

query:
	python -m lab.run_query $(Q)
