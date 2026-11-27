F ?= queries/all_prereqs.cypher
CODE ?= MATH201

load:
	poetry run python -m prereq.load

query:
	poetry run python -m prereq.cli $(F) code=$(CODE)
