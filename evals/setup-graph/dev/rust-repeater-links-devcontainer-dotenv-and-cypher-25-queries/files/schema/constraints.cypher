CREATE CONSTRAINT repeater_callsign IF NOT EXISTS FOR (r:Repeater) REQUIRE r.callsign IS UNIQUE;
