MATCH (f:Family) WHERE f.email ENDS WITH '@schoolrun-qa.test' DETACH DELETE f;
