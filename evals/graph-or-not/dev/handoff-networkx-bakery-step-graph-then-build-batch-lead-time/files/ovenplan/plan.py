"""Morning planning screen."""
import sqlite3

DB = "var/recipes.db"


def todays_products(conn, day):
    return conn.execute(
        "SELECT r.id, r.name, p.batches FROM daily_plan p JOIN recipe r ON r.id = p.recipe_id WHERE p.day = ? ORDER BY r.name",
        (day,)).fetchall()


def screen(day):
    conn = sqlite3.connect(DB)
    try:
        rows = []
        for recipe_id, name, batches in todays_products(conn, day):
            # TODO: lead time per product, so the shift lead knows when to start it
            rows.append({"recipe": name, "batches": batches, "lead_time": None})
        return rows
    finally:
        conn.close()
