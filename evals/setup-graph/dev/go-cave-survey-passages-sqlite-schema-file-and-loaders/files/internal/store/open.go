// Package store opens the survey database.
package store

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

// Open returns a handle on the SQLite file. Writers and readers share it; readOnly opens it with mode=ro.
func Open(path string, readOnly bool) (*sql.DB, error) {
	dsn := "file:" + path + "?_busy_timeout=5000&_journal_mode=WAL"
	if readOnly {
		dsn += "&mode=ro"
	}
	return sql.Open("sqlite3", dsn)
}
