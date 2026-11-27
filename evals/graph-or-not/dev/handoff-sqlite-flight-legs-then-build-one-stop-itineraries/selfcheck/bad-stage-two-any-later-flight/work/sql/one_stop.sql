SELECT f1.id AS first_flight_id, f2.id AS second_flight_id
FROM flight f1 JOIN flight f2 ON f2.origin = f1.dest
WHERE f1.origin = :origin AND date(f1.dep_utc) = :day AND f2.dest = :dest AND f2.dep_utc > f1.arr_utc;
