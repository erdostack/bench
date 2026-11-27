Added page_order(conn, policy_id). Our escalation rule is at most 3 escalations, so the list holds up to 4
policies, and it stops early when a policy repeats.
