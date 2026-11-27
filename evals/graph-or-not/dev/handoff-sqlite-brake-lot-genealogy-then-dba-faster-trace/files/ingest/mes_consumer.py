"""Consumes lot-link events from a plant's MES topic and writes them to lot_link."""


def handle(conn, event):
    conn.execute(
        "INSERT INTO lot_link (parent_lot, child_lot, qty, linked_at) VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING",
        (event["parent"], event["child"], event["qty"], event["at"]))
