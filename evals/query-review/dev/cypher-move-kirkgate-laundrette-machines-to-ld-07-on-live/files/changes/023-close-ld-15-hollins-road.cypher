// 023: LD-15 Hollins Road closed 2026-06-30 (lease ended). Machines re-sited separately in 024.
MATCH (s:Shop {code: 'LD-15'}) SET s.open = false;
