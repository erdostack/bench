The PRAC-SAT- practice trees are out of the training graph, along with their links. The PRAC-BASE trees and the course streets and volunteers are still there.

What was removed from the training graph (`data/training.json`):
- 41 PRAC-SAT- tree nodes
- 41 `on_street` links from those trees
- 101 `surveyed` links from volunteers to those trees

Training graph after the change: 60 PRAC-BASE trees, 4 PRAC-ST- streets, 12 volunteers, 60 `on_street` links and 125 `surveyed` links. Every remaining link points to a node that is still there.

The published graph (`data/published.json`) was not touched. It is the council's public tree map, and it is written only by their nightly export.
