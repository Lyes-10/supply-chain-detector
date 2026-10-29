import sys
import os
import glob

sys.path.insert(0, os.path.dirname(__file__))
from detector import scan_package

test_dir = os.path.expanduser("~/supply-chain-project/test-packages")
package_jsons = glob.glob(os.path.join(test_dir, "*", "package.json"))

results = []
for pj in package_jsons:
    pkg_name = os.path.basename(os.path.dirname(pj))
    score, findings = scan_package(pkg_name, pj)
    results.append((pkg_name, score, findings))

print("\n\n=== SUMMARY ===")
for name, score, findings in results:
    verdict = "SUSPICIOUS" if score >= 4 else "LOW RISK" if score > 0 else "CLEAN"
    print(f"{name:20s} score={score:3d}  verdict={verdict}")
