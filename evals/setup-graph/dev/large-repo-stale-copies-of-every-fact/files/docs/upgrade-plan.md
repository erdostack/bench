# Plan: move to a calendar-version Neo4j

Status: draft, not scheduled.

## Why

The 5.x line only receives fixes. The features we want for the provenance work (and the language changes that come
with them) are only in the calendar-version releases.

## Target

Neo4j 2026.x, with the collection database switched to Cypher 25 once every saved query has been checked.

## Steps

1. Rewrite the saved queries that use syntax Cypher 25 drops. Candidates are collected in `queries/drafts/`, each
   prefixed with `CYPHER 25` so that it can be tried on a scratch 2026.x server without changing that server's
   default.
2. Bump the driver to the 6.x line and fix the deprecations.
3. Upgrade the development server, then the shared one.
4. Switch the database default from Cypher 5 to Cypher 25 and drop the prefixes from the drafts as they replace
   the originals.

## Not started

All of the above except a few drafts.
