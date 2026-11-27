# Clients

| Client | Protocol | Notes |
|---|---|---|
| PC (launcher 5.x) | sync v2, JSON | timestamps as ISO-8601 UTC strings |
| Mobile 2.x | sync v2, JSON | same as PC |
| Console 3.x | sync v1, binary | timestamps as unix seconds; the sync service stores fields as received |

When a match ends, the client of the host reports the squad; the sync service upserts `played_with` for
every pair in it (games + 1, last_played = the match end time from the report).
