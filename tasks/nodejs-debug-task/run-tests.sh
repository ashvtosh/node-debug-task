#!/usr/bin/env bash
set -euo pipefail

# Ensure tests deps installed in the container running this script
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true

# Run pytest
python3 -m pytest -q tests/test_outputs.py