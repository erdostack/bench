# Roast: vaultshelf queries

Reviewed against the isolation rule in the README: a user must learn nothing about another workspace.

## Findings

### 1. duplicates_of (critical)

**Problem.** The first MATCH ties the starting file to the caller's workspace. The second goes from that file to its Blob and back out to every File with the same content, and returns id, name and folder for each. Nothing restricts those other files to the caller's workspace, and docs/model.md states that a Blob belongs to no workspace because identical content is stored once for the whole service. A user can therefore upload a standard form (or any document they are curious about) and read the file names and folder paths under which other customers hold it. Folder names in this product are things like client and matter names.

**Fix.** Scope the far end as well: MATCH (f)-[:HAS_CONTENT]->(b:Blob)<-[:HAS_CONTENT]-(other:File)-[:IN]->(:Workspace {id: $ws}), or add AND other.ws = $ws. Add a test with the same content uploaded in two workspaces.

### 2. list_folder (low)

**Problem.** Relies on the File.ws property where the other queries go through the IN relationship. add_file sets both from the same Workspace node and nothing changes them later, so they agree; it is two ways of asking the same thing.

**Fix.** Leave it; note in the model doc that File.ws is the copy used for the folder index.

### 3. remove_file (low)

**Problem.** Deleting the last file that points at a Blob leaves the Blob behind.

**Fix.** A periodic sweep of Blobs with no files, if storage should be reclaimed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
