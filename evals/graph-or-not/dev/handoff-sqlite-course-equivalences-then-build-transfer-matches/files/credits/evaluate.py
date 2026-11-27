"""Transfer credit evaluation screen for advisors."""
from . import sql


def evaluate(conn, course_id: int) -> dict:
    course = sql.fetch(conn, "course.sql", course_id=course_id)
    if not course:
        raise LookupError(course_id)
    code, title, credits, institution = course[0]
    # TODO: list every course this one is equivalent to (registrar's rules)
    return {"code": code, "title": title, "credits": credits, "institution": institution, "equivalents": []}
