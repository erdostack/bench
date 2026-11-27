# Building

Versions of third-party libraries are set once, in the parent `pom.xml`. Modules never write a `<version>` for
a managed dependency; if you need a new library, add it to the parent's `dependencyManagement` first.

`./mvnw -q install -DskipTests` builds both modules. `bin/cypher` compiles what it needs by itself.
