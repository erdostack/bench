# Onboarding

1. Install Docker, Node 22, Python 3.12, JDK 21 and Go 1.24. Yes, all of them; or only the ones for your service.
2. `make up` at the repository root starts the shared infrastructure.
3. Read the README of the service you will work on. The root README is a map, not a manual.
4. Passwords for local containers come from environment variables; ask your team lead for the values and keep
   them out of the repository.

## Graph queries

Routing people: `make mgq FILE=...` from the root, or `mgconsole` directly.

Everyone else: you probably do not need the graph. If you think you do, talk to the network team first.
