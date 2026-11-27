.PHONY: analyze test

analyze:
	python -m castgraph.analyze summary
	python -m castgraph.analyze brokers --top 10

test:
	python -m pytest -q
