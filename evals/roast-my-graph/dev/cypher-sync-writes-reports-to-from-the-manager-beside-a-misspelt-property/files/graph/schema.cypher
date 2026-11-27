CREATE CONSTRAINT employee_staff_no IF NOT EXISTS FOR (e:Employee) REQUIRE e.staff_no IS UNIQUE;
CREATE CONSTRAINT team_code IF NOT EXISTS FOR (t:Team) REQUIRE t.code IS UNIQUE;
CREATE CONSTRAINT site_code IF NOT EXISTS FOR (s:Site) REQUIRE s.code IS UNIQUE;

CREATE INDEX tmp_idx_2 IF NOT EXISTS FOR (e:Employee) ON (e.managment_level);
