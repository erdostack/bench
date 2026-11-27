# citeweb

A reading-group tool: which papers cite which, and what should we read before the one on the agenda.

The citation graph is an embedded LadybugDB database (a directory under `var/`, created by `just load`). There
is no server and no container.

    uv sync
    just load
    just query queries/read_first.cypher
