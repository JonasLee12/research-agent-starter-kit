# Retrieval Protocol

Use retrieval to find project memory and source metadata. Do not treat retrieval as proof that a source supports a claim.

## Retrieval Layers

1. Source register and readiness matrix.
2. Keyword search over local files.
3. Dependency-free local SQLite index and FTS/hashed retrieval.
4. Optional ChromaDB neural vector retrieval when installed.
5. Self-growing knowledge-base navigation through `raw-inbox`, `growth-queue`, and `compiled-wiki`.
6. Human source-section review.

## Local Tools

| Tool | Use | Dependency Boundary |
|---|---|---|
| `scripts/build_agent_index.py` | Builds a SQLite index of project memory, headings, evidence markers, and session events | Python standard library |
| `scripts/local_retrieval_search.py` | Runs FTS and hashed-vector retrieval over local Markdown/text files | Python standard library |
| `scripts/kb_health_check.py` | Checks self-growing KB structure and private-data boundary markers | Python standard library |
| `scripts/build_vector_index.py` | Builds optional ChromaDB neural vector index | Requires `requirements-vector.txt` |
| `scripts/vector_retrieval_smoke_test.py` | Runs known-query smoke tests for optional vector retrieval | Requires `requirements-vector.txt` |

## Use Rules

- Metadata-only records are not citation-ready.
- Retrieved chunks must be checked against the original source note or document.
- Claim support requires source-section review.
- Private data, transcripts, consent forms, and restricted materials must not be indexed into public or shareable layers.
- Generated SQLite, vector, and runtime index files under `.agent-runtime/` are local state and should not be committed.

## Minimum Output

When retrieval informs formal writing, record:

- query;
- files or records retrieved;
- evidence readiness status;
- what still needs human verification.
