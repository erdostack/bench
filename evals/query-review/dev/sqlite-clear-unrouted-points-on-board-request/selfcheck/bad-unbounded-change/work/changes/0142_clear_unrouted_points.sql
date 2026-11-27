DELETE FROM points WHERE id NOT IN (SELECT point FROM stops);
