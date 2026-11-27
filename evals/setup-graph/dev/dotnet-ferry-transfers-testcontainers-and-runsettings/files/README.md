# ferrylink

Transfer planning over a generated ferry timetable: ports, and a SAILS_TO link per direct sailing.

There is no standing database. The test project starts a throwaway Neo4j in Docker through Testcontainers,
loads data/*.csv into it and runs the queries: Neo4j 5.26.24, the default in
tests/Ferry.Graph.Tests/GraphContainer.cs.

    dotnet test                                   # unit and query tests
    make q F=queries/transfers.cypher             # one ad-hoc query, rows printed to the console

Package versions are central (Directory.Packages.props) and locked (packages.lock.json).
