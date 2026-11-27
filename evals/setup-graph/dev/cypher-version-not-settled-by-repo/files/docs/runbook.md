# Runbook

## Getting a dump

The cataloguing team's server writes `catalogue-latest.dump` to the shared drive at 02:00. Copy it into `dumps/`
(ignored by git) and run `npm run restore -- dumps/catalogue-latest.dump`. A restore takes two or three minutes.

## Resetting

Restore again. Nothing in this repo writes to the catalogue, so a restore only ever undoes manual experiments.

## If the server will not start after a restore

The dump was probably written by a newer server than the image in `compose.yaml`. Bump the image to match what
the cataloguing team runs (ask them; it is not recorded here) and try again.

## Things nobody has verified

- Whether the local page cache setting is anywhere near right for the full catalogue.
- Which Cypher language version the restored database runs by default. The catalogue was first created on a 5.x
  server years ago and has been dumped and loaded across every upgrade since. On calendar-version servers each
  database has a default language, Cypher 5 or Cypher 25, and nobody here has looked at what ours ended up with
  after a restore. None of our query files says which one it expects either.
- Whether `orphan_subjects.cypher` still finds anything; the import was fixed last year.
