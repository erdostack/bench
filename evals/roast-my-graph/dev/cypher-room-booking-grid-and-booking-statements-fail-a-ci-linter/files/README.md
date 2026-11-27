# deskgrid

Meeting room booking for our 9 office buildings. Neo4j 5.26.

    model/model.md          labels and relationships
    model/schema.cypher     constraints and indexes
    queries/grid.cypher     the Today screen
    queries/book.cypher     booking and cancelling

The Today screen shows one grid per building: a row per room, a column per half-hour slot from 08:00
to 17:30 (20 slots), each cell free or taken.

## Sizes

- 9 buildings, 230 rooms; the largest building has 46 rooms
- Slot: 20 nodes, fixed (08:00, 08:30, ... 17:30)
- Booking: only today and the next 13 days are kept in the graph; a nightly job moves older bookings
  to the archive. About 9,000 bookings at any time, about 1,500 new ones a day.
