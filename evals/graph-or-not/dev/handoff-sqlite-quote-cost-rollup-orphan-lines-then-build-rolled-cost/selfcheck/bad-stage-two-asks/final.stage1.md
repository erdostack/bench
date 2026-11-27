Decision: recursive-sql

A 7-level rollup over 31,000 BOM lines, 200 times a day: one recursive query on the SQLite file. A graph database
doesn't fix the purged rows; turning on PRAGMA foreign_keys in the loader does.
