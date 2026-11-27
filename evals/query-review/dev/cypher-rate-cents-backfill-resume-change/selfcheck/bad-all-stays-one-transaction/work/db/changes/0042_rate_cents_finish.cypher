MATCH (s:Stay)
SET s.rateCents = toInteger(round(s.nightlyRate * 100));
