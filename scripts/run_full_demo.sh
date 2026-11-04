#!/bin/bash
set -e

# ---- EDIT THIS ONE LINE IF KALI'S IP CHANGES ----
KALI_IP="192.168.42.128"
# --------------------------------------------------

REGISTRY="http://${KALI_IP}:4873"
REPO_URL="https://github.com/Lyes-10/supply-chain-detector.git"

echo "=================================================="
echo " RESETTING ENVIRONMENT (safe to rerun any time)"
echo "=================================================="
rm -rf ~/victim-test
rm -rf ~/supply-chain-project
rm -f ~/safe-install.sh
rm -f /tmp/supply_chain_demo_marker.txt
mkdir -p ~/victim-test
echo "Environment reset complete."

echo ""
echo "=================================================="
echo " PART 1 - Installing reqeusts with NO protection"
echo "=================================================="
cd ~/victim-test
npm init -y > /dev/null
npm install reqeusts --registry "$REGISTRY"

echo ""
echo "--- Proof of compromise ---"
cat /tmp/supply_chain_demo_marker.txt
echo ""
read -p "Press Enter to deploy the scanner from GitHub..."

echo ""
echo "=================================================="
echo " PART 2 - Cloning the scanner from GitHub"
echo "=================================================="
git clone "$REPO_URL" ~/supply-chain-project
pip install python-Levenshtein --break-system-packages --quiet

echo ""
echo "=================================================="
echo " PART 3 - Setting up the safe-install wrapper"
echo "=================================================="
cat > ~/safe-install.sh << EOS
#!/bin/bash
REGISTRY="${REGISTRY}"
python3 ~/supply-chain-project/detector/safe_install.py "\$1" "\$REGISTRY"
EOS
chmod +x ~/safe-install.sh
echo "safe-install.sh ready, pointed at $REGISTRY"
echo ""
read -p "Press Enter to re-attempt install, now WITH protection..."

echo ""
echo "=================================================="
echo " PART 4 - Re-installing reqeusts WITH protection"
echo "=================================================="
rm -rf ~/victim-test
mkdir -p ~/victim-test
cd ~/victim-test
rm -f /tmp/supply_chain_demo_marker.txt
~/safe-install.sh reqeusts || true

echo ""
echo "--- Checking whether the payload ran this time ---"
if [ -f /tmp/supply_chain_demo_marker.txt ]; then
    echo "MARKER FILE EXISTS - install was NOT blocked (unexpected!)"
else
    echo "No marker file found - install was correctly BLOCKED. System protected."
fi

echo ""
echo "=================================================="
echo " Demo finished. Run this script again any time -"
echo " it resets everything itself, nothing to clean up."
echo "=================================================="
