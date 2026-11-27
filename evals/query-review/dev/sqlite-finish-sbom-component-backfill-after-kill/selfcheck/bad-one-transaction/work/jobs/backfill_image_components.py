def run(conn):
    with conn:
        conn.execute("DELETE FROM image_component")
        conn.execute("""INSERT INTO image_component (image_id, component_id)
                        SELECT DISTINCT e.image_id, c.id FROM sbom_entry e JOIN component c ON c.purl = e.purl""")
        conn.execute("UPDATE image SET component_count = (SELECT count(*) FROM image_component ic WHERE ic.image_id = image.id)")
    return conn.execute("SELECT count(*) FROM image").fetchone()[0]
