I have written the archive change for airlog and rehearsed it on the rehearsal copy. I have not applied it to airlog: the station engineer applies change files overnight, after review.

The change is changes/0008_archive_episodes_before_2024.sql. It archives the 554 episodes aired before 2024-01-01, which is the cut-off the programme committee set for 2026. Each run moves the next 30 episodes and every edge touching them at either end, as docs/archive.md describes. Pilots never broadcast (12 of them) are left alone, as the docs say.

I did not copy last year's file, changes/0007. It only moves edges where the episode is the source, so it would leave behind the 52 repeat_of edges that point from a newer repeat into an older episode, and those would be left pointing at deleted nodes. The new file moves edges at both ends.

Rehearsal result: the file ran in 19 runs and changed 19,366 rows. Afterwards no episodes before 2024 remain live, the archive holds 1,093 episodes, and no live edge points at a missing node. The edge counts match: 13,384 live plus 17,941 archived is 31,325, the same as before.

One thing for the programme team to decide before it goes to airlog: once these episodes are archived, the 52 newer repeat broadcasts lose their repeat_of link to the original in the live tables. The archive keeps the link, but the listen-again pages will not show it. The docs say to archive edges at both ends, so I followed them, but the team should confirm that is what they want.

Overnight, the station engineer can run: bin/apply airlog changes/0008_archive_episodes_before_2024.sql
