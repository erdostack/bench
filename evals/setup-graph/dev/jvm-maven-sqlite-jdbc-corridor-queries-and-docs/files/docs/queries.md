# Query files

- One statement per file in `queries/`, numbered `?1` placeholders for arguments.
- Written for SQLite 3.45, so use its full join support where it makes a query clearer.
- Recursive CTEs carry the path as text and stop at 12 hops; corridors form cycles.
- Survey years are columns `y2024` / `y2025` on `corridor`, 1 when a crossing was recorded.
