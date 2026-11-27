// INC-2950: a test agent was visible on the site.
MATCH (a:Agent {agentId: 'ag-test-0001'}) SET a.hidden = true;
