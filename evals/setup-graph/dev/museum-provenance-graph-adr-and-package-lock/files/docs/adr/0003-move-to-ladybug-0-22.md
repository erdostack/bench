# 3. Move to LadybugDB 0.22.3

Status: accepted (2026-11-10)

## Context

Version 0.22 changes the on-disk format, so the database in var/ has to be rebuilt from data/ after the
upgrade (`npm run load`).

## Decision

We run @ladybugdb/core 0.22.3. Loading and querying code does not change.

## Consequences

Everyone runs `npm ci && npm run load` once after pulling the change.
