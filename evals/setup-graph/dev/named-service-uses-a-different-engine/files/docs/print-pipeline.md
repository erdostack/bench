# Print pipeline

1. GIS export lands in `services/atlas/export/`.
2. `npm run build-graph -w services/atlas` rebuilds the path network file.
3. The layout tool calls `route()` for each suggested walk and draws the result.

Step 2 is the only step that writes the file. Nothing else should.
