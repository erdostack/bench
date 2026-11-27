No, leave it as it is. Neither of those is an orphan in this model (docs/model.md):

- A Departure is the timetable entry for a tour on a date, shared by every booking on it. When a
  cancelled booking's legs go, the departure is still there for everyone else who booked it, and if it now
  has no legs it's simply unbooked, which is what most future departures look like. The site sells seats
  from it. Deleting "departures without legs" would take unbooked tours off sale.
- A Customer is a login. People keep their account after cancelling, and about half of all customers
  have no booking at a given moment. Deleting them would delete accounts.

What does belong to a booking is its legs (each is exactly one traveller's seat in that booking), and
the job already deletes those with it. DETACH DELETE on the legs removes their ON relationships, so the
departures' seat counts go back up, which is what you want.

If you want to confirm nothing is left hanging, the only real orphan would be a leg with no booking:
`MATCH (l:Leg) WHERE NOT EXISTS { (:Booking)-[:HAS_LEG]->(l) } RETURN count(l)` should be 0 after a run.
