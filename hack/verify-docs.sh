#!/usr/bin/env bash
set -euo pipefail

uv run --group docs python scripts/generate_aap_docs.py --check
