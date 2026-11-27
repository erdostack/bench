// name: reset_board
MATCH (b:Board {id: $board_id})<-[:ON_BOARD]-(c:Card)
MATCH (l:Label)
WHERE l.name STARTS WITH 'tmp-'
DETACH DELETE c, l;

// name: export_card_titles
MATCH (c:Card)-[:ON_BOARD]->(b:Board {id: $board_id})
RETURN c.id AS id, c.title AS title, c.status AS status
ORDER BY c.position;

// name: cards_with_any_label
MATCH (b:Board {id: $board_id})<-[:ON_BOARD]-(c:Card)-[:TAGGED]->(l:Label)
WHERE l.name IN $label_names
RETURN count(DISTINCT c) AS cards;

// name: open_cards
MATCH (c:Card)-[:ON_BOARD]->(b:Board {id: $board_id})
WHERE c.status <> 'archived'
RETURN c.id AS id, c.title AS title
ORDER BY c.position;

// name: board_labels
MATCH (l:Label)-[:LABEL_FOR]->(b:Board {id: $board_id})
RETURN l.id AS id, l.name AS name, l.colour AS colour
ORDER BY l.name;
