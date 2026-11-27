# Target graph export

`ci/export_graph.sh` writes one JSON object:

```json
{
  "targets": {
    "//payments/core:lib": {"kind": "library", "deps": ["//common/money:lib"], "tools": ["//tools/protoc:bin"]},
    "//payments/core:test": {"kind": "test", "deps": ["//payments/core:lib"], "tools": []},
    "//tools/protoc:bin": {"kind": "binary", "deps": [], "tools": []}
  }
}
```

- `kind` is one of `library`, `binary`, `test`.
- `deps`: targets this one links against or imports.
- `tools`: targets that are run while building this one (code generators, compilers, linters built in-repo).
- Every name in `deps` and `tools` is a key of `targets`.
