# brackenford-pools

The pools graph of Brackenford Leisure Trust in Neo4j: the four pools, every timetabled session, who
teaches it and who booked it. The booking app, the poolside screens and the timetable import read it.

- `bin/bl live "<cypher>"` or `bin/bl live --file <file.cypher>`: send Cypher to the database.
- `changes/`: data changes, one file each, named after their ticket: `changes/<TICKET>-<what>.cypher`.
- `docs/database.md`: the database and how a change gets in. `docs/model.md`: labels, types, counts.
  `docs/archiving.md`: what the year-end archive does.
