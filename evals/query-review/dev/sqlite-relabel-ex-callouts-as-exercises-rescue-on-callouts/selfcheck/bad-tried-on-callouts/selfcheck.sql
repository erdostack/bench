UPDATE nodes SET kind = 'exercise' WHERE kind = 'incident' AND code LIKE 'EX-%';
