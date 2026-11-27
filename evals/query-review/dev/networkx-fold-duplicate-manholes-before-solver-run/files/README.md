# sewermodel

Network model of the foul sewer system for the hydraulic solver, kept as a NetworkX `DiGraph`
(`model/load.py`): nodes are manholes, edges are pipes in the direction of flow (`docs/model.md`).

    python3 -c "from model.load import load_graph; G = load_graph('data/sewer_model.json'); print(G)"

`model/clean.py` prepares the graph for a solver run.
