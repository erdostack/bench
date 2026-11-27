"""Remove a workspace and everything in it, in one transaction, and record that it was done."""

DELETE_CARDS = """
MATCH (:Workspace {id: $workspace_id})-[:HAS_BOARD]->(:Board)-[:HAS_LIST]->(:List)-[:HAS_CARD]->(c:Card)
DETACH DELETE c
"""

DELETE_LISTS_AND_LABELS = """
MATCH (:Workspace {id: $workspace_id})-[:HAS_BOARD]->(:Board)-[:HAS_LIST|HAS_LABEL]->(x)
DETACH DELETE x
"""

DELETE_BOARDS = """
MATCH (:Workspace {id: $workspace_id})-[:HAS_BOARD]->(b:Board)
DETACH DELETE b
"""

DELETE_WORKSPACE = """
MATCH (w:Workspace {id: $workspace_id})
DETACH DELETE w
"""

RECORD_AUDIT = """
CREATE (:AuditEvent {kind: 'workspace_offboarded', workspace_id: $workspace_id, actor: $actor, at: datetime()})
"""


def _offboard(tx, workspace_id, actor):
    for statement in (DELETE_CARDS, DELETE_LISTS_AND_LABELS, DELETE_BOARDS, DELETE_WORKSPACE):
        tx.run(statement, workspace_id=workspace_id).consume()
    tx.run(RECORD_AUDIT, workspace_id=workspace_id, actor=actor).consume()


def offboard(driver, workspace_id, actor):
    with driver.session(database="pinboard") as session:
        session.execute_write(_offboard, workspace_id, actor)
