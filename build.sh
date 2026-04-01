#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -n "${GITHUB_PAGES_BASEPATH:-}" ]]; then
  BASEPATH="$GITHUB_PAGES_BASEPATH"
else
  REPO_NAME="$(basename "$SCRIPT_DIR")"
  BASEPATH="/${REPO_NAME}/"
fi

python3 -m src.main "$BASEPATH"
