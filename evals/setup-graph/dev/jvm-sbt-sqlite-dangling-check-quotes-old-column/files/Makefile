.PHONY: q check

q:
	sbt -batch "runMain ferrylink.Sql $(F)"

check:
	sbt -batch "runMain ferrylink.Sql checks/dangling.sql"
