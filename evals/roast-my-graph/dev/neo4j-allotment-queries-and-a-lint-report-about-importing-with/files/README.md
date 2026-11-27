# plotkeeper

Waiting lists and plot assignments for a city's allotment gardens.
`(:Applicant)-[:WAITING_FOR {since}]->(:Site)`, `(:Site)-[:HAS_PLOT]->(:Plot)<-[:TENANT_OF {from}]-(:Applicant)`.
~60 sites, 9,000 plots, 14,000 applicants on waiting lists.
