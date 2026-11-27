# Writing queries

- Files in `queries/` are Cypher 25, the server's default language, so they carry no version prefix.
- Parameters are passed as `key=value` after the file name and arrive as strings.
- Keep variable-length patterns bounded: the board graph has a few very connected directors.
