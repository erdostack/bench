"""Plan limits. Every create in api/ calls one of these before it writes."""

MAX_BOARDS_PER_WORKSPACE = 10
MAX_LISTS_PER_BOARD = 12
MAX_LABELS_PER_BOARD = 40
MAX_CARDS_PER_BOARD = 300  # archived cards count


class LimitReached(Exception):
    pass


def check_new_board(tx, workspace_id):
    n = tx.run("MATCH (:Workspace {id: $w})-[:HAS_BOARD]->(b:Board) RETURN count(b) AS n", w=workspace_id).single()["n"]
    if n >= MAX_BOARDS_PER_WORKSPACE:
        raise LimitReached("boards")


def check_new_card(tx, board_id):
    n = tx.run("MATCH (:Board {id: $b})-[:HAS_LIST]->(:List)-[:HAS_CARD]->(c:Card) RETURN count(c) AS n",
               b=board_id).single()["n"]
    if n >= MAX_CARDS_PER_BOARD:
        raise LimitReached("cards")


def check_new_label(tx, board_id):
    n = tx.run("MATCH (:Board {id: $b})-[:HAS_LABEL]->(l:Label) RETURN count(l) AS n", b=board_id).single()["n"]
    if n >= MAX_LABELS_PER_BOARD:
        raise LimitReached("labels")
