# metroline

The tram network of a mid-sized city as a graph: lines, stations, fare zones, and the tap-ins from the
ticket gates. Neo4j 5.

    model/schema.cypher      constraints and indexes
    model/model.md           labels and relationships
    queries/planner.cypher   used by the journey planner app
    queries/reports.cypher   used by the reporting jobs

## Size

| Thing | Count |
|---|---|
| `Line` | 9 |
| `Station` | 212 |
| `Zone` | 6 |
| `Tap` | 1.6 million a day, 13 months kept (about 620 million) |

## Who runs what

- planner.cypher: `same_line` and `station_board` on every search in the app, a few hundred a second at
  rush hour. `zone_pairs` fills the fare table on the admin screen.
- reports.cypher: `busiest_stations` every night for the previous day. `line_ridership` on the first of
  each month, once per line, for the report that goes to the city's transport board; it decides which
  stations get staff and which lose them.
