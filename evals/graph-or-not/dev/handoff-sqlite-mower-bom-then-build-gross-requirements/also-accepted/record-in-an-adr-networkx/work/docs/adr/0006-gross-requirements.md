# ADR 0006: gross requirements on the works-order screen

Status: accepted, 2026-11-24

Decision: in-process-library

Context: 48,000 items and 210,000 BOM lines, deepest BOM 11 levels, about 300 explosions a day, 3 s
allowed. A recursive query on a copy took 0.4 s.

Rule from the planning lead: 4% scrap on every BOM line, compounding down the levels.

Not a graph database: nothing here needs one.
