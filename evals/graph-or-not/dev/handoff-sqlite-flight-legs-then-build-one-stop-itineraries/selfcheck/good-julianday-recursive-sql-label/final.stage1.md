Decision: recursive-sql

One stop, never two, is a single join: flights leaving the origin on the day, joined to flights leaving their
arrival airport for the destination between 50 minutes and 5 hours after landing. Notes in docs/graph/DECISION.md.

- 5,800 flights a day with `flight_by_origin` makes that a few index probes per search; 40 searches a second is
  nothing for SQLite read-only, and far inside 300 ms.
- A graph database would be a second copy of the timetable to rebuild every night, for a query of fixed depth one.
  Route networks are graphs, but this rule never walks them.
- If revenue management ever allows two stops or asks for the best route over any number, that is a path search
  and worth revisiting.
