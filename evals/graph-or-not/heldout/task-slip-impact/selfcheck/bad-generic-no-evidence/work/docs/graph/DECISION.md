Decision: recursive-sql

Transitive dependencies need recursion, which a plain join cannot express, but SQLite supports recursive
CTEs, so a graph database is unnecessary.
