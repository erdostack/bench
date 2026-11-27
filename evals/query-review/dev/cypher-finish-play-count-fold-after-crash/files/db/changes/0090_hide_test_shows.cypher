MATCH (s:Show) WHERE s.slug STARTS WITH 'qa-test-' SET s.hidden = true;
