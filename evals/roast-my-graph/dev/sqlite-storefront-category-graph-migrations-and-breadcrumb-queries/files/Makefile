db:
	rm -f shop.db
	for f in migrations/*.sql; do sqlite3 shop.db < $$f; done
