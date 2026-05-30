#!/usr/bin/env bash
set -euo pipefail

cat <<'MSG'
Vector retrieval is optional.

To use it, install:

  pip install -r requirements-vector.txt

This script builds a local ChromaDB index under `.agent-runtime/`.
Generated vector databases are private runtime state and are not committed.
MSG

python3 scripts/build_vector_index.py --rebuild --summary
python3 scripts/vector_retrieval_smoke_test.py
