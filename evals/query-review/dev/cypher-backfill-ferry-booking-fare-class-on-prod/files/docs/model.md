# Model (Neo4j 5.26)

    (:Booking {ref, createdAt, fareClass, vehicle, passengers})-[:ON]->(:Sailing {sailingId, departs})
    (:Booking)-[:MADE_BY]->(:Account {accountNo})

| Property | Type |
|---|---|
| `Booking.ref` | STRING, `KS-7Q4M2D` |
| `Booking.createdAt` | DATETIME (UTC) |
| `Booking.fareClass` | STRING, see `docs/fares.md`; absent on some bookings made before 2026-03-01 |
| `Booking.vehicle` | STRING (`car`, `van`, `motorcycle`, `bicycle`), absent for foot passengers |
| `Booking.passengers` | INTEGER |
| `Sailing.departs` | DATETIME (UTC) |

About 310,000 bookings: about 236,000 made before 2026-03-01 and 74,000 since. About 9,000 sailings
(about 34 bookings each, at most 60) and 88,000 accounts (most have a few bookings; the largest, a haulier,
has 1,150).
