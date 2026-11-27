# townmap

Open map tooling for a town council: a places catalogue with opening hours and accessibility notes, and an
offline router for the printed walking maps.

## Stack

- Node 22, npm workspaces
- Graph database: Neo4j 2025.10.1 (see `compose.yaml`)
- Everything is TypeScript-free on purpose; plain ES modules.

## Workspaces

| Workspace | Purpose |
|---|---|
| `services/catalog` | places API |
| `services/atlas` | offline routing for the print pipeline |
| `packages/shared` | logging and small helpers |

    npm ci
    docker compose up -d
    npm test --workspaces
