use std::collections::HashMap;

use petgraph::graph::{NodeIndex, UnGraph};
use serde::Deserialize;

#[derive(Deserialize)]
struct Cabinet { id: String, zone: String }

#[derive(Deserialize)]
struct Duct { from: String, to: String, metres: u32 }

pub struct Network {
    pub graph: UnGraph<String, u32>,
    pub index: HashMap<String, NodeIndex>,
    pub zone: HashMap<String, String>,
}

pub fn network(cabinets: &str, ducts: &str) -> Result<Network, Box<dyn std::error::Error>> {
    let mut graph = UnGraph::new_undirected();
    let mut index = HashMap::new();
    let mut zone = HashMap::new();
    for row in csv::Reader::from_path(cabinets)?.deserialize() {
        let c: Cabinet = row?;
        index.insert(c.id.clone(), graph.add_node(c.id.clone()));
        zone.insert(c.id, c.zone);
    }
    for row in csv::Reader::from_path(ducts)?.deserialize() {
        let d: Duct = row?;
        graph.add_edge(index[&d.from], index[&d.to], d.metres);
    }
    Ok(Network { graph, index, zone })
}
