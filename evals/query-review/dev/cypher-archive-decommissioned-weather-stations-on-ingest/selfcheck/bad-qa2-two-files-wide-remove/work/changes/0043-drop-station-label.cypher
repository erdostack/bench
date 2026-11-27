// archive step 2
MATCH (s:Station {status: 'decommissioned'})
REMOVE s:Station;
