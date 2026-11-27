F ?= sql/ancestry.sql
ARGS ?=

.PHONY: q report test

q:
	sbt -batch "runMain propagation.Sql $(F) $(ARGS)"

report:
	for f in sql/reports/*.sql; do sbt -batch "runMain propagation.Sql $$f"; done

test:
	sbt -batch test
