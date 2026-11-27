SELECT service_id, station_code
FROM departure
WHERE date(scheduled) = :service_date AND actual IS NOT NULL
  AND (CAST(substr(actual, 12, 2) AS INTEGER) * 60 + CAST(substr(actual, 15, 2) AS INTEGER))
    - (CAST(substr(scheduled, 12, 2) AS INTEGER) * 60 + CAST(substr(scheduled, 15, 2) AS INTEGER)) >= 5;
