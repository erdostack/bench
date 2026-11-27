# Year-end archive

Before the new year's timetable is imported, every session that started before 1 January of the new year
is archived: the node gets the `:ArchivedSession` label and loses `:Session`. An archive changes labels
only. No property is added or changed, no relationship is touched and nothing is deleted, because the
reports join bookings to archived sessions.

Swim School sessions (`programme = 'school'`) are never archived by the year-end archive: the badge audit
reads them from the timetable, and the Swim School team archives them itself after its audit.
