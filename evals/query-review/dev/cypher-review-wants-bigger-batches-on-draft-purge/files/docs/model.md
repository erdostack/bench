# Graph model

    (:Matter {id, title})
    (:Draft {id, title, status, lastEditedAt})        status: active | filed | abandoned
    (:Authority {cite})                                 cases and statutes
    (:Comment {id, body, at})
    (:ShareLink {token, expiresAt})                     standalone, no relationships
    (:Draft)-[:FOR]->(:Matter)
    (:Draft)-[:CITES {pinpoint}]->(:Authority)
    (:Draft)-[:ANNOTATED {span, note}]->(:Authority)
    (:Comment)-[:ON]->(:Draft)
    (:Draft)-[:REVISION_OF]->(:Draft)

Relationships per draft: median 35. Long briefs reach the caps the editor enforces: at most 250 CITES and
ANNOTATED together, at most 60 comments (each with its ON), plus FOR and one REVISION_OF, so a single
draft can have up to 312 relationships; with its comments it is at most 373 nodes and relationships.
Abandoned drafts are often the long ones (a brief that was started over).

Comments belong to their draft and are deleted with it.
