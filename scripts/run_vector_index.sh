#!/usr/bin/env bash
set -euo pipefail

cat <<'MSG'
Vector retrieval is optional.

To use it, install:

  pip install -r requirements-vector.txt

This starter script is intentionally conservative. It does not build an index
until you add or implement a local vector-index workflow for your project.
MSG
