#!/bin/bash
set -e
cd ~/supply-chain-project/detector

echo "=================================================="
echo " PART 2a - Single package scan (reqeusts)"
echo "=================================================="
python3 detector.py

echo ""
echo "=================================================="
echo " PART 2b - Scan all 3 malicious demo packages"
echo "=================================================="
python3 -c "
import sys, os, glob
sys.path.insert(0, '.')
from detector import scan_package

mal_dir = os.path.expanduser('~/supply-chain-project/malicious-packages')
for pj in glob.glob(os.path.join(mal_dir, '*', 'package.json')):
    name = os.path.basename(os.path.dirname(pj))
    scan_package(name, pj)
"

echo ""
echo "=================================================="
echo " PART 2c - Full evaluation report (precision/recall/F1)"
echo "=================================================="
python3 ~/supply-chain-project/detector/eval_metrics.py

echo ""
echo "=================================================="
echo " Report complete. Safe to rerun any time - read-only."
echo "=================================================="
