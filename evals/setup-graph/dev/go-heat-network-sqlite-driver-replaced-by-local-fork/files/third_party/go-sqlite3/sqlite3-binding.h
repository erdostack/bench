#ifndef USE_LIBSQLITE3
/*
** Public interface of the SQLite library, copied from the amalgamation (sqlite3.h).
** Kept next to sqlite3-binding.c; see FORK.md for when it was last refreshed.
*/
#ifndef SQLITE3_H
#define SQLITE3_H
#include <stdarg.h>

#ifdef __cplusplus
extern "C" {
#endif

#define SQLITE_VERSION        "3.47.2"
#define SQLITE_VERSION_NUMBER 3047002

typedef struct sqlite3 sqlite3;
typedef struct sqlite3_stmt sqlite3_stmt;

const char *sqlite3_libversion(void);
const char *sqlite3_sourceid(void);
int sqlite3_libversion_number(void);

int sqlite3_open_v2(const char *filename, sqlite3 **ppDb, int flags, const char *zVfs);
int sqlite3_prepare_v2(sqlite3 *db, const char *zSql, int nByte, sqlite3_stmt **ppStmt, const char **pzTail);
int sqlite3_step(sqlite3_stmt *pStmt);
int sqlite3_finalize(sqlite3_stmt *pStmt);
int sqlite3_close_v2(sqlite3 *db);

#ifdef __cplusplus
}
#endif
#endif /* SQLITE3_H */
#else
#include <sqlite3.h>
#endif
