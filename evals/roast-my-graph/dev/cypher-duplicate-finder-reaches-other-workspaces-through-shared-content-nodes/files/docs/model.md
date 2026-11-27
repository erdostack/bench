# Model

| Node | Key | Notes |
|---|---|---|
| `Workspace` | `id` | one per customer |
| `User` | `id` | `(:User)-[:MEMBER_OF]->(:Workspace)`, exactly one |
| `File` | `id` | `(:File)-[:IN]->(:Workspace)`, exactly one; has `name`, `folder`, `uploaded_at` |
| `Blob` | `sha256` | the stored bytes; has `size_bytes` |

| Relationship | From | To |
|---|---|---|
| `HAS_CONTENT` | `File` | `Blob` |
| `SHARED_WITH` | `File` | `User` |
| `UPLOADED` | `User` | `File` |

## Blobs are stored once

Identical content is stored once for the whole service. When an upload has a sha256 we already hold, the new
`File` points at the existing `Blob` and nothing is written to object storage. A `Blob` therefore belongs to
no workspace: the same standard form, court template or software manual is typically held by hundreds of
customers. This saves about 41% of storage.
