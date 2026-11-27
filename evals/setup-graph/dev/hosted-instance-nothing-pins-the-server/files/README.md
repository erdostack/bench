# skilltree

Learning-path explorer for an apprenticeship programme: skills, the skills they build on, and the workshops that
teach them.

The graph is a hosted Neo4j (AuraDB) instance shared by the whole programme team. There is no local database
and no container: ask the programme office for a login and put it in a local `.env` (see `env.sample`).

    npm ci
    npm run cypher -- cypher/path_to_skill.cypher
