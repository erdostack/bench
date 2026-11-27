"""Reviewer picker for the editor's assignment page."""
from . import db


def candidates(conn, submission_id: int, topic: str, limit: int = 50) -> list[dict]:
    authors = {r[0] for r in db.rows(conn, "submission_authors.sql", submission_id=submission_id)}
    picked = []
    for researcher_id, name, papers in db.rows(conn, "reviewers_by_topic.sql", topic=topic, limit=limit * 2):
        if researcher_id in authors:
            continue
        # TODO: hide reviewers with a conflict of interest (editor-in-chief's rule)
        picked.append({"id": researcher_id, "name": name, "papers": papers})
    return picked[:limit]
