#!/usr/bin/env bash
# DA-Shield - Group 31. Run with:  bash run_mac_linux.sh
set -e
cd "$(dirname "$0")"
PY=python3; command -v $PY >/dev/null 2>&1 || PY=python
echo "[1/4] Installing libraries..."
$PY -m pip install -r requirements.txt || $PY -m pip install --user -r requirements.txt
echo "[2/4] Running Modules A, B and C (full evaluation)..."
$PY src/dashield_prototype.py > outputs/run_log.txt
echo "      Results saved to outputs/results.json"
echo "[3/4] Drawing figures..."
$PY src/make_figures.py
echo "      Figures saved to outputs/figures"
echo "[4/4] Opening the interactive demo..."
$PY src/dashield_demo.py
