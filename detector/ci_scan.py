import sys
import os
import json
import glob

sys.path.insert(0, os.path.dirname(__file__))
from detector import scan_package

SCAN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scan-targets")

def main():
    package_jsons = glob.glob(os.path.join(SCAN_DIR, "*", "package.json"))

    if not package_jsons:
        print("No packages found to scan in scan-targets/")
        sys.exit(0)

    any_suspicious = False
    for pj in package_jsons:
        with open(pj) as f:
            pkg_data = json.load(f)
        pkg_name = pkg_data.get("name", os.path.basename(os.path.dirname(pj)))

        score, findings = scan_package(pkg_name, pj)
        if score >= 4:
            any_suspicious = True

    print("\n=== CI SCAN RESULT ===")
    if any_suspicious:
        print("BLOCKED: one or more packages flagged as SUSPICIOUS.")
        sys.exit(1)
    else:
        print("PASSED: no suspicious packages found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
