# Query style

- Every query file is written for Cypher 25, the default language of the release line our server is
  on, so files carry no `CYPHER` prefix.
- Parameters, never string concatenation.
- One query per file; the file name says what it returns.
- Bound every variable-length pattern (`*1..6`), the leg graph has cycles through the hubs.
