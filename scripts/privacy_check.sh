#!/usr/bin/env bash
set -euo pipefail

echo "Running privacy check..."

# This script checks for high-risk concrete leaks.
# Add project-specific private names, emails, module URLs, and local paths to .privacy-patterns.
DEFAULT_PATTERNS=(
  "BEGIN RSA"
  "BEGIN OPENSSH"
  "OPENAI_CREDENTIAL"
  "sk-[A-Za-z0-9]{20,}"
  "ghp_[A-Za-z0-9]{20,}"
  "github_pat_"
  "xox[baprs]-"
  "AKIA[0-9A-Z]{16}"
  "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
  "${HOME%/*}/[A-Za-z0-9._-]+"
  "C:\\\\Users\\\\[A-Za-z0-9._-]+"
)

PATTERNS=("${DEFAULT_PATTERNS[@]}")
ALLOWLIST_PATTERNS=(
  "your\\.email@university\\.ac\\.uk"
)

if [[ -f .privacy-patterns ]]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    PATTERNS+=("$line")
  done < .privacy-patterns
fi

FOUND=0
for pattern in "${PATTERNS[@]}"; do
  MATCHES="$(grep -RInE "$pattern" . \
    --exclude-dir=.git \
    --exclude-dir=.obsidian \
    --exclude-dir=.codex \
    --exclude-dir=.agent-runtime \
    --exclude-dir=audit-reports \
    --exclude-dir=research-wiki/skill-evals \
    --exclude-dir=research-wiki/runtime-receipts \
    --exclude-dir=research-wiki/material-passports \
    --exclude-dir=research-wiki/pre-delivery-locks \
    --exclude=.DS_Store \
    --exclude=privacy_check.sh \
    --exclude=.privacy-patterns.example || true)"
  for allowed in "${ALLOWLIST_PATTERNS[@]}"; do
    MATCHES="$(printf "%s\n" "$MATCHES" | grep -Ev "$allowed" || true)"
  done
  if [[ -n "$MATCHES" ]]; then
    printf "%s\n" "$MATCHES"
    FOUND=1
  fi
done

if [[ "$FOUND" -eq 1 ]]; then
  echo "Privacy check found possible sensitive content. Review before pushing."
  echo "Tip: add project-specific patterns to .privacy-patterns and keep that file local/private."
  exit 1
fi

echo "Privacy check passed."
