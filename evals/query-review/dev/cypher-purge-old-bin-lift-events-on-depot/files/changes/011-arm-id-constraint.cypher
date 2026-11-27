// why: FLT-88 arms are identified by armId; the gateway relies on it.
// changes: one constraint. count: SHOW CONSTRAINTS YIELD name WHERE name = 'arm_id' RETURN count(*);
CREATE CONSTRAINT arm_id IF NOT EXISTS FOR (a:Arm) REQUIRE a.armId IS UNIQUE;
