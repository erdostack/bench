MATCH (:Router)-[s:PEERS_WITH]->(:Router)
RETURN count(s) AS sessions;
