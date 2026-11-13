#!/bin/bash
set -e
cd ~/supply-chain-project
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Retry helper: runs a command up to 5 times, waiting 5s between attempts
retry() {
    local n=1
    local max=5
    local delay=5
    while true; do
        "$@" && return 0
        if [ $n -ge $max ]; then
            echo "Command failed after $n attempts: $*"
            return 1
        fi
        echo "Attempt $n/$max failed. Retrying in ${delay}s..."
        n=$((n+1))
        sleep $delay
    done
}

echo "=================================================="
echo " Resetting to a clean main branch"
echo "=================================================="
git checkout main
retry git pull origin main

echo ""
echo "=================================================="
echo " SCENARIO A — Clean dependency push (should PASS)"
echo "=================================================="
CLEAN_BRANCH="ci-demo-clean-${TIMESTAMP}"
git checkout -b "$CLEAN_BRANCH"

mkdir -p "scan-targets/clean-test-${TIMESTAMP}"
cat > "scan-targets/clean-test-${TIMESTAMP}/package.json" << EOJSON
{
  "name": "clean-test-${TIMESTAMP}",
  "version": "1.0.0",
  "description": "benign test package for CI demo"
}
EOJSON

git add "scan-targets/clean-test-${TIMESTAMP}"
git commit -m "Demo: add benign dependency (clean-test-${TIMESTAMP})"
retry git push origin "$CLEAN_BRANCH"

retry gh pr create --base main --head "$CLEAN_BRANCH" \
  --title "Demo: benign dependency (${TIMESTAMP})" \
  --body "Clean CI demo run."

echo "Waiting for CI to start..."
sleep 5
retry gh pr checks "$CLEAN_BRANCH" --watch || true

read -p "Press Enter to continue to Scenario B (malicious push)..."

echo ""
echo "=================================================="
echo " SCENARIO B — Malicious dependency push (should FAIL)"
echo "=================================================="
git checkout main
MAL_BRANCH="ci-demo-malicious-${TIMESTAMP}"
git checkout -b "$MAL_BRANCH"

mkdir -p "scan-targets/reqeusts-${TIMESTAMP}"
cp demo-malicious-pkg/package.json "scan-targets/reqeusts-${TIMESTAMP}/"
cp demo-malicious-pkg/marker.js "scan-targets/reqeusts-${TIMESTAMP}/"

python3 - << PYEOF
import json
p = "scan-targets/reqeusts-${TIMESTAMP}/package.json"
with open(p) as f:
    data = json.load(f)
data["name"] = "reqeusts"
with open(p, "w") as f:
    json.dump(data, f, indent=2)
PYEOF

git add "scan-targets/reqeusts-${TIMESTAMP}"
git commit -m "Demo: add malicious typosquatted dependency (reqeusts-${TIMESTAMP})"
retry git push origin "$MAL_BRANCH"

retry gh pr create --base main --head "$MAL_BRANCH" \
  --title "Demo: malicious dependency (${TIMESTAMP})" \
  --body "Malicious CI demo run — this PR should be blocked by the scanner."

echo "Waiting for CI to start..."
sleep 5
retry gh pr checks "$MAL_BRANCH" --watch || true

echo ""
echo "=================================================="
echo " CLEANUP — closing demo PRs and deleting branches"
echo "=================================================="
retry gh pr close "$CLEAN_BRANCH" --delete-branch || true
retry gh pr close "$MAL_BRANCH" --delete-branch || true
git checkout main
git branch -D "$CLEAN_BRANCH" "$MAL_BRANCH" 2>/dev/null || true

echo ""
echo "Demo complete. main is clean, both demo branches/PRs removed."
echo "You can run this script again right now — nothing to reset manually."
