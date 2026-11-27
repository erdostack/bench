# ADR 0004: Move to the 6.x Java driver

Status: Accepted (2026-06-02)

## Decision

We move the service to neo4j-java-driver 6.1.0, managed in our own pom instead of through the Spring
Boot parent, so that driver upgrades are not tied to Boot upgrades.

## Consequences

- Reactive session code in `LoanRoutes` must be rewritten to the new API.
