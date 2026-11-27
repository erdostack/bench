// COL-301: unique round codes, needed by the CrewLink round picker.
CREATE CONSTRAINT round_code IF NOT EXISTS FOR (r:Round) REQUIRE r.code IS UNIQUE;
