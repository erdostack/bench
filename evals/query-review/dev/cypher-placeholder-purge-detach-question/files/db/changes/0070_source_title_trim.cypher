MATCH (s:Source) WHERE s.title STARTS WITH ' ' SET s.title = trim(s.title);
