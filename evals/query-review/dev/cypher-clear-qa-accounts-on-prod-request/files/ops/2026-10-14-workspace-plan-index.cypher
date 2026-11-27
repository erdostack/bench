// TB-2210: admin console filters workspaces by plan. Reviewed by d.ferro, run by on-call 2026-10-14.
CREATE INDEX workspace_plan IF NOT EXISTS FOR (w:Workspace) ON (w.plan);
