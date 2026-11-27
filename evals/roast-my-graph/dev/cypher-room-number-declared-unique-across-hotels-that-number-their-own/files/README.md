# innkeep

Availability and bookings for a hotel group. Neo4j 5.

    graph/schema.cypher     constraints and indexes
    graph/load.cypher       loads hotels and rooms from the property system (run when a hotel joins or
                            refurbishes; rows arrive as `$rows`)
    graph/booking.cypher    what the booking engine runs; each statement has a `// name:` line
    data/sample/            first rows of the property system's export

## Numbers

340 hotels, 61,000 rooms, about 9 million bookings a year. `free_rooms` is the search behind the booking
page (peak 250 calls a second); `book_room` runs about 25,000 times a day.

The group grew by buying hotels, so nothing about the properties is standardised: each hotel has its own
floor plan, its own rate classes and its own room numbering.
