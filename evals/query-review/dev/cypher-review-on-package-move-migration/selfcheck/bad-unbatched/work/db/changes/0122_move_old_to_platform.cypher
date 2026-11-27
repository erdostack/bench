// BLD-501: //old/... moved to //platform/... in the repo; rename the targets to match.
MATCH (t:Target) WHERE t.label STARTS WITH '//old/'
SET t.label = '//platform/' + substring(t.label, 6);
