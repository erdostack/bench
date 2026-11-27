# ADR 004: tags are flat labels

**Status:** accepted · **Date:** 2024-02-06

## Context

Editors want to find pictures by subject. We looked at a category tree (as the old DAM had) and at free
tags.

## Decision

Free tags, no hierarchy. A tag is a label; an asset has any number of them. Nobody on the desk has time
to maintain a tree, and the old one was ignored.

## Consequences

- Two tables, `tags` and `asset_tags`.
- "Assets with tag X" is one indexed lookup. No special storage or search technology is needed for tags.
