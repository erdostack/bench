"""Course page data."""
from advising.db import rows


def course_page(conn, course_id):
    (code, title, level), = rows(conn, "course.sql", course_id=course_id)
    listed = rows(conn, "listed_prerequisites.sql", course_id=course_id)
    needed = rows(conn, "all_prerequisites.sql", course_id=course_id)
    return {"code": code, "title": title, "level": level, "listed": listed, "needed": needed}
