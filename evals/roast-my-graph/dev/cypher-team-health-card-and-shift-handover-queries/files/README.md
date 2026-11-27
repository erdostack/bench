# pagerline

On-call scheduling and incident tracking for the platform org. The graph lives in Neo4j 5.26; the web
app reads it through the statements in `queries/`.

    model/schema.cypher       constraints and indexes
    model/model.md            labels and relationships
    queries/cards.cypher      the team page (one statement per card)
    queries/handover.cypher   shift handover

## Sizes (November 2026)

| Thing | Count |
|---|---|
| Team | 340 |
| Person | 4,100; a team has 4 to 31 members, median 12 |
| Incident | about 160,000 in the graph (closed incidents move to the warehouse 120 days after closing); in the last 90 days the busiest team opened 9,400, the median team 310 |
| ON_CALL | shifts for the next 30 days, about 60 per team |

## Who reads what

The team page runs every statement in `cards.cypher` on each view, about 40 views a second in office
hours. From next quarter engineering managers quote the health card ("12 people, 310 incidents in 90
days, 4 sev1") in the staffing review. `hand_over_shift` runs when the person on call hands the rest
of a shift to someone else.
