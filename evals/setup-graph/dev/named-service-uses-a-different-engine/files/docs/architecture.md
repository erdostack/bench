# Architecture

The places catalogue is the system of record and lives in the council's Neo4j instance. `services/catalog` is
the only thing that talks to it.

`services/atlas` has no network at run time. It works from a file that the print pipeline rebuilds from the GIS
export before each edition of the map.

`packages/shared` must stay dependency-free.
