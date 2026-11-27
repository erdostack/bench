//! lendq <file.cypher>: run one read query against the lending graph, print rows as JSON lines.
use neo4rs::{query, Graph};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let uri = std::env::var("GRAPH_URI").unwrap_or_else(|_| "bolt://graph-next:7687".into());
    let file = std::env::args().nth(1).ok_or("usage: lendq <file.cypher>")?;
    let text = tokio::fs::read_to_string(&file).await?;
    let graph = Graph::new(&uri, "", "").await?;
    let mut rows = graph.execute(query(&text)).await?;
    while let Some(row) = rows.next().await? {
        println!("{}", row.to::<serde_json::Value>().map(|v| v.to_string()).unwrap_or_default());
    }
    Ok(())
}
