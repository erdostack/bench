-- Departures that did not run on :service_date.
SELECT service_id, station_code
FROM departure
WHERE date(scheduled) = :service_date AND actual IS NULL
ORDER BY service_id, station_code;
