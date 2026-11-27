# ADR 0004: escalation path for the alert page

Status: accepted, 2026-11-23

Decision: recursive-sql

Context: 3,100 policies (2,700 escalate somewhere), chains up to 9 policies, 46 loops between teams. The SRE
leads' rule: at most 4 escalations (5 policies counting the first), then the incident commander rota; a policy
already paged is never paged again, so a loop ends the path.

Consequences: one recursive query over the config file with a path guard and a step limit. No Neo4j.
