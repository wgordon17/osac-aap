#!/usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null || { echo "uv not found in PATH"; exit 1; }

uv run --group docs python scripts/generate_aap_docs.py
