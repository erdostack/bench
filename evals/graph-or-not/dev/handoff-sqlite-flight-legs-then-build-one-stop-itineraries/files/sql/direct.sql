-- Direct flights for a search. :origin, :dest, :day (ISO date, UTC departure day)
SELECT id
FROM flight
WHERE origin = :origin
  AND dest = :dest
  AND date(dep_utc) = :day
ORDER BY dep_utc;
