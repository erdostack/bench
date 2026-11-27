CREATE CONSTRAINT parcel_tracking_no IF NOT EXISTS FOR (p:Parcel) REQUIRE p.tracking_no IS UNIQUE;
CREATE CONSTRAINT depot_code IF NOT EXISTS FOR (d:Depot) REQUIRE d.code IS UNIQUE;
CREATE CONSTRAINT route_id IF NOT EXISTS FOR (r:Route) REQUIRE r.id IS UNIQUE;

CREATE INDEX parcel_depot_status IF NOT EXISTS FOR (p:Parcel) ON (p.depot_code, p.status);
