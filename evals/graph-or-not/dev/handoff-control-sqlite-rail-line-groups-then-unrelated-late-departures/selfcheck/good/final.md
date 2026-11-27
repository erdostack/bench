Added sql/late_departures.sql: departures whose scheduled date is :service_date, that ran, and left at least 5 minutes late (julianday difference, so a train that leaves after midnight still counts).
