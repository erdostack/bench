CUTOFF = "2025-07-01"


def run(conn):
    with conn:
        conn.execute("CREATE TEMP TABLE gone AS SELECT id FROM players WHERE status = 'trialist' AND trial_ended < ?", (CUTOFF,))
        conn.execute("""CREATE TEMP TABLE gone_agents AS SELECT DISTINCT r.agent_id AS id FROM represents r
                        WHERE r.player_id IN (SELECT id FROM temp.gone) AND NOT EXISTS (SELECT 1 FROM represents o
                        WHERE o.agent_id = r.agent_id AND o.player_id NOT IN (SELECT id FROM temp.gone))""")
        conn.execute("DELETE FROM represents WHERE player_id IN (SELECT id FROM temp.gone)")
        n = conn.execute("DELETE FROM players WHERE id IN (SELECT id FROM temp.gone)").rowcount
        conn.execute("DELETE FROM agents WHERE id IN (SELECT id FROM temp.gone_agents)")
    return n
