Wrote queries/friends.sql: the member's friendships from both columns of person_knows_person, newest first, with
friend_id and since. Per docs/graph/DECISION.md, friends whose account is closed are left out (account_state label
'closed'); suspended accounts still show.
