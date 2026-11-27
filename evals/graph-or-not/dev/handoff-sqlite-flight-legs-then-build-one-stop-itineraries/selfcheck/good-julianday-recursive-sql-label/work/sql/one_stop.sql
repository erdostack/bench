select a.id as first_flight_id, b.id as second_flight_id
from flight a, flight b
where a.origin = :origin and b.dest = :dest and b.origin = a.dest
  and substr(a.dep_utc, 1, 10) = :day
  and (julianday(b.dep_utc) - julianday(a.arr_utc)) * 1440 between 50 and 300
