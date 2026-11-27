use neo4rs::{query, Graph};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = std::env::args().nth(1).ok_or("usage: groundq <file.cypher>")?;
    let text = std::fs::read_to_string(file)?;
    let graph = Graph::new("localhost:7687", "", "").await?;
    let mut rows = graph.execute(query(&text)).await?;
    while let Some(row) = rows.next().await? {
        println!("{:?}", row);
    }
    Ok(())
}
