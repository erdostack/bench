# borders

Which municipalities share a border, and how long it is, for the regional planning office. Neo4j 5.26.

`import/borders.csv` comes from the national survey and lists every shared border from both sides: once
under each municipality, with the same length. `load/load_borders.cypher` keeps one `BORDERS`
relationship per pair, always from the lower code to the higher one. A border has no direction; the
arrow only exists because Neo4j stores one.

About 340 municipalities and 1,900 borders.
