// archive step 2: drop Station from the stations tagged in 0042
MATCH (s:Station:ArchivedStation)
REMOVE s:Station;
