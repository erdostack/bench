"""0029: move the waitlist places too."""
def run(conn):
    with conn:
        return conn.execute("UPDATE edges SET dst = (SELECT r.dst FROM edges r WHERE r.kind = 'relieved_by' AND r.src = edges.dst) "
                            "WHERE kind = 'waitlisted_on' AND dst IN (SELECT src FROM edges WHERE kind = 'relieved_by')").rowcount
