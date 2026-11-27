# Model

- `(:Room {id, name})-[:ON_FLOOR]->(:Floor {id, level})-[:IN]->(:Building {code, name})`
- `(:Booking {cell, day, created_at})-[:FOR_ROOM]->(:Room)`
- `(:Booking)-[:AT]->(:Slot {start})`
- `(:Person {id, name})-[:BOOKED]->(:Booking)`

`Booking.cell` is room id, day and slot start joined with `|`, for example `R-114|2026-11-24|09:30`.
It is unique, so a second booking of the same room, day and slot fails.
