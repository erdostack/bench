.PHONY: test q

test:
	dotnet test

q:
	QUERY_FILE=$(abspath $(F)) dotnet test tests/Ferry.Graph.Tests --filter Category=AdHoc --logger "console;verbosity=detailed"
