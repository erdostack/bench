//! Copies the open part of the trail network out of Postgres into a SQLite file for the reach tool.
use rusqlite::{params, Connection};
use sqlx::{postgres::PgPoolOptions, Row};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let out = std::env::args().nth(1).expect("usage: snapshot <out.sqlite>");
    let url = std::env::var("DATABASE_URL").unwrap_or_else(|_| "postgres://trailhub@localhost/trailhub".into());
    let pg = PgPoolOptions::new().connect(&url).await?;
    let _ = std::fs::remove_file(&out);
    let mut lite = Connection::open(&out)?;
    lite.execute_batch(include_str!("../sqlite_schema.sql"))?;
    let tx = lite.transaction()?;
    for row in sqlx::query("SELECT id, name, kind FROM junction").fetch_all(&pg).await? {
        tx.execute("INSERT INTO junction VALUES (?1, ?2, ?3)",
                   params![row.get::<i64, _>(0), row.get::<String, _>(1), row.get::<String, _>(2)])?;
    }
    for row in sqlx::query("SELECT id, a, b, km::float8 FROM segment WHERE is_open").fetch_all(&pg).await? {
        tx.execute("INSERT INTO segment VALUES (?1, ?2, ?3, ?4)",
                   params![row.get::<i64, _>(0), row.get::<i64, _>(1), row.get::<i64, _>(2), row.get::<f64, _>(3)])?;
    }
    tx.commit()?;
    Ok(())
}
